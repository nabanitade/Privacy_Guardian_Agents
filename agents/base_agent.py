"""
Base Agent - Foundation for Privacy Guardian Multi-Agent System
==============================================================

This module provides the foundational BaseAgent class that all Privacy Guardian agents inherit from.
It implements the core functionality for event-based communication, AI integration, logging, and
agent lifecycle management using Google Cloud Agent Development Kit (ADK) patterns.

Key Features:
------------
- Event-based communication system for agent collaboration
- Google Gemini AI integration with fallback mechanisms
- Comprehensive logging and activity tracking
- Agent lifecycle management and status reporting
- Common utilities for file operations and data processing

Event System:
------------
The base agent provides the event publishing infrastructure that enables the event-based architecture:
- publish_event(): Publish events for other agents to consume
- Event tracking and correlation ID management
- Event history for debugging and monitoring

AI Integration:
--------------
- Google Gemini AI integration with automatic availability detection
- Fallback mechanisms when AI is unavailable
- Context-aware AI analysis with structured prompts
- Error handling and graceful degradation

Agent Lifecycle:
---------------
- Agent initialization and configuration
- Status reporting and health monitoring
- Activity logging with different severity levels
- Correlation ID tracking for request tracing

Usage:
------
All Privacy Guardian agents inherit from BaseAgent and use its core functionality:

```python
from .base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("my_agent", "🤖 MyAgent")
    
    async def process(self, input_data):
        # Agent-specific processing logic
        # Use self.publish_event() to emit events
        # Use self.get_gemini_analysis() for AI enhancement
        pass
```

Event-Based Architecture:
------------------------
The Privacy Guardian system uses events for agent communication:
- PrivacyScanAgent emits FindingsReady
- GeminiAnalysisAgent emits AIEnhancedFindings  
- ComplianceAgent emits ComplianceAnalysisCompleted
- FixSuggestionAgent emits FixSuggestionsCompleted
- ReportAgent emits ReportGenerated

Dependencies:
------------
- google.generativeai: Google Gemini AI integration
- asyncio: Asynchronous processing
- logging: Activity logging and monitoring
- datetime: Timestamp management
- typing: Type hints and data structures

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)
"""

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, UTC
import json
from google.cloud.logging_v2.handlers import StructuredLogHandler

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from google.cloud import logging as cloud_logging
from google.cloud import bigquery
from google.cloud import secretmanager
from google.cloud import monitoring_v3

# Gemini imports with fallback
try:
    from google.cloud import aiplatform
    from vertexai.generative_models import GenerativeModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Set up structured logging for Google Cloud
logging.basicConfig(level=logging.INFO, handlers=[StructuredLogHandler()])

@dataclass
class AgentEvent:
    """
    Standardized event structure for inter-agent communication.
    
    Attributes:
        event_type: Type of event (e.g., "ScanStarted", "ViolationDetected")
        agent_id: ID of the agent that published the event
        timestamp: UTC timestamp when event was created
        data: Event-specific data payload
        correlation_id: Request correlation ID for tracing
    """
    event_type: str
    agent_id: str
    timestamp: datetime
    data: Dict[str, Any]
    correlation_id: str

@dataclass
class ScanResult:
    """
    Standardized scan result structure for privacy violations.
    
    Attributes:
        file_path: Path to the file containing the violation
        line_number: Line number where violation was detected
        violation_type: Type of privacy violation (e.g., "HardcodedEmail")
        description: Human-readable description of the violation
        severity: Severity level (HIGH, MEDIUM, LOW)
        fix_suggestion: Suggested fix for the violation
        regulation_reference: Applicable regulations (GDPR, CCPA, etc.)
        agent_id: ID of the agent that detected the violation
        timestamp: When the violation was detected
    """
    file_path: str
    line_number: int
    violation_type: str
    description: str
    severity: str  # HIGH, MEDIUM, LOW
    fix_suggestion: str
    regulation_reference: str
    agent_id: str
    timestamp: datetime

class BaseAgent(ABC):
    """
    Base class for all Privacy Guardian Agents with Gemini AI integration.
    
    This class provides the foundation for all agents in the privacy compliance
    system. It includes AI capabilities, event handling, logging, and common
    functionality that all agents need.
    
    Key Responsibilities:
    - Initialize and manage Gemini AI integration
    - Handle event publishing and consumption
    - Provide structured logging and monitoring
    - Manage agent status and health
    - Handle errors and provide fallback mechanisms
    
    AI Integration:
    - Automatically initializes Gemini when Google Cloud credentials are available
    - Provides get_gemini_analysis() method for AI-powered processing
    - Gracefully falls back to hardcoded rules when AI is unavailable
    - Manages token limits and response parsing
    
    Event System:
    - publish_event(): Publish events for other agents to consume
    - consume_event(): Consume events from other agents
    - Event history tracking for monitoring and debugging
    
    Logging:
    - Google Cloud Logging integration with local fallback
    - Structured logging with agent context
    - Activity tracking and performance monitoring
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        """
        Initialize the base agent with AI capabilities and logging.
        
        Args:
            agent_id: Unique identifier for this agent
            agent_name: Human-readable name for this agent
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.logger = self._setup_logging()
        self.events_published: List[AgentEvent] = []
        self.events_consumed: List[AgentEvent] = []
        self.gemini_model = None
        self._initialize_gemini()
        self.bigquery_client = self._initialize_bigquery()
        self.secret_manager_client = self._initialize_secret_manager()
        self.monitoring_client = self._initialize_monitoring()
        
    def _initialize_gemini(self):
        """
        Initialize Google Gemini AI for the agent.
        
        Attempts to initialize Gemini AI using Google Cloud credentials.
        Falls back gracefully if credentials are not available or initialization fails.
        """
        if not GEMINI_AVAILABLE:
            self.logger.warning("Gemini AI not available - using hardcoded rules only")
            return
            
        try:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
            
            if project_id:
                aiplatform.init(project=project_id, location=location)
                self.gemini_model = GenerativeModel("gemini-2.0-flash")
                self.logger.info(f"✅ Gemini AI initialized for {self.agent_name}")
            else:
                self.logger.warning("GOOGLE_CLOUD_PROJECT not set - Gemini AI disabled")
                
        except Exception as e:
            self.logger.warning(f"Failed to initialize Gemini AI: {str(e)} - using hardcoded rules")
            self.gemini_model = None
    
    async def get_gemini_analysis(self, prompt: str, context: Dict[str, Any] = None) -> Optional[str]:
        """
        Get AI analysis from Google Gemini with fallback.
        
        Args:
            prompt: The prompt to send to Gemini AI
            context: Optional context data to include with the prompt
            
        Returns:
            AI response text if successful, None if AI is unavailable or fails
            
        Note:
            This method automatically handles token limits, error handling,
            and fallback mechanisms. If AI is not available, it returns None
            and the calling agent should use hardcoded rules.
        """
        if not self.gemini_model:
            self.logger.debug("Gemini not available - using hardcoded rules")
            return None
            
        try:
            # Enhance prompt with context if provided
            if context:
                context_str = json.dumps(context, indent=2)
                enhanced_prompt = f"{prompt}\n\nContext:\n{context_str}"
            else:
                enhanced_prompt = prompt
                
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                enhanced_prompt,
                generation_config={
                    "max_output_tokens": 2000,
                    "temperature": 0.1
                }
            )
            
            self.logger.info(f"🤖 Gemini analysis completed for {self.agent_name}")
            return response.text
            
        except Exception as e:
            self.logger.warning(f"Gemini analysis failed: {str(e)} - using hardcoded rules")
            return None
    
    def is_gemini_available(self) -> bool:
        """
        Check if Gemini AI is available for this agent.
        
        Returns:
            True if Gemini AI is initialized and available, False otherwise
        """
        return self.gemini_model is not None
        
    def _setup_logging(self) -> logging.Logger:
        """
        Setup logging for the agent using StructuredLogHandler.
        
        Uses Google Cloud's StructuredLogHandler for production-grade logging.
        Falls back to local logging if Cloud Logging is not available.
        
        Returns:
            Configured logger instance
        """
        try:
            # Use StructuredLogHandler (already configured globally)
            logger = logging.getLogger(f"privacy_guardian.{self.agent_id}")
            logger.setLevel(logging.INFO)
            return logger
        except Exception as e:
            # Fallback to local logging if Cloud Logging fails
            logging.basicConfig(level=logging.INFO)
            return logging.getLogger(f"privacy_guardian.{self.agent_id}")
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Main processing method that each agent must implement.
        
        This is the core method that each derived agent must implement.
        It defines the agent's primary functionality and processing logic.
        
        Args:
            input_data: Input data for processing (format depends on agent type)
            
        Returns:
            Processing results (format depends on agent type)
        """
        pass
    
    def publish_event(self, event_type: str, data: Dict[str, Any], correlation_id: str) -> AgentEvent:
        """
        Publish an event for other agents to consume.
        
        Creates and stores an event that can be consumed by other agents.
        Events are used for inter-agent communication and workflow coordination.
        
        Args:
            event_type: Type of event being published
            data: Event-specific data payload
            correlation_id: Request correlation ID for tracing
            
        Returns:
            Created AgentEvent instance
        """
        event = AgentEvent(
            event_type=event_type,
            agent_id=self.agent_id,
            timestamp=datetime.now(UTC),
            data=data,
            correlation_id=correlation_id
        )
        self.events_published.append(event)
        self.logger.info(f"📤 Published event: {event_type} with correlation_id: {correlation_id}")
        return event
    
    def consume_event(self, event: AgentEvent) -> None:
        """
        Consume an event from another agent.
        
        Processes an event received from another agent. This method can be
        overridden by derived agents to implement specific event handling logic.
        
        Args:
            event: The event to consume
        """
        self.events_consumed.append(event)
        self.logger.info(f"📥 Consumed event: {event.event_type} from {event.agent_id}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status for monitoring.
        
        Returns a dictionary containing the agent's current status,
        including AI availability, event counts, and activity information.
        
        Returns:
            Dictionary with agent status information
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": "active",
            "events_published": len(self.events_published),
            "events_consumed": len(self.events_consumed),
            "gemini_available": self.is_gemini_available(),
            "last_activity": datetime.now(UTC).isoformat()
        }
    
    def log_activity(self, message: str, level: str = "info") -> None:
        """
        Log agent activity with structured logging.
        
        Provides structured logging with agent context for monitoring
        and debugging purposes.
        
        Args:
            message: Activity message to log
            level: Log level (info, warning, error, debug)
        """
        log_data = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "message": message,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        if level == "info":
            self.logger.info(json.dumps(log_data))
        elif level == "warning":
            self.logger.warning(json.dumps(log_data))
        elif level == "error":
            self.logger.error(json.dumps(log_data))
        elif level == "debug":
            self.logger.debug(json.dumps(log_data))

    def _initialize_bigquery(self):
        """
        Initialize BigQuery client for analytics.
        """
        try:
            client = bigquery.Client()
            self.log_activity("BigQuery client initialized successfully")
            return client
        except Exception as e:
            self.log_activity(f"Failed to initialize BigQuery: {str(e)}", "warning")
            return None

    def _initialize_secret_manager(self):
        """
        Initialize Secret Manager client for secure config.
        """
        try:
            client = secretmanager.SecretManagerServiceClient()
            self.log_activity("Secret Manager client initialized successfully")
            return client
        except Exception as e:
            self.log_activity(f"Failed to initialize Secret Manager: {str(e)}", "warning")
            return None

    def _initialize_monitoring(self):
        """
        Initialize Cloud Monitoring client for custom metrics.
        """
        try:
            client = monitoring_v3.MetricServiceClient()
            self.log_activity("Cloud Monitoring client initialized successfully")
            return client
        except Exception as e:
            self.log_activity(f"Failed to initialize Cloud Monitoring: {str(e)}", "warning")
            return None

    def insert_bigquery_analytics(self, table_id: str, rows: list):
        """
        Insert analytics data into BigQuery table.
        Args:
            table_id: Full BigQuery table ID (project.dataset.table)
            rows: List of dictionaries to insert
        """
        if not self.bigquery_client:
            self.log_activity("BigQuery client not available", "warning")
            return False
        if not rows:
            self.log_activity("No rows to insert into BigQuery, skipping.", "info")
            return True
        try:
            serializable_rows = []
            for row in rows:
                if hasattr(row, '__dict__'):
                    serializable_row = {}
                    for key, value in row.__dict__.items():
                        if isinstance(value, datetime):
                            serializable_row[key] = value.isoformat()
                        else:
                            serializable_row[key] = value
                    serializable_rows.append(serializable_row)
                else:
                    serializable_row = {}
                    for key, value in row.items():
                        if isinstance(value, datetime):
                            serializable_row[key] = value.isoformat()
                        else:
                            serializable_row[key] = value
                    serializable_rows.append(serializable_row)
            try:
                errors = self.bigquery_client.insert_rows_json(table_id, serializable_rows)
                if errors == []:
                    self.log_activity(f"Inserted {len(serializable_rows)} rows into BigQuery: {table_id}")
                    return True
                else:
                    self.log_activity(f"BigQuery insert errors: {errors}", "warning")
                    return False
            except Exception as table_error:
                if "Not found" in str(table_error):
                    self.log_activity(f"BigQuery table {table_id} not found - skipping analytics", "warning")
                    return False
                else:
                    raise table_error
        except Exception as e:
            self.log_activity(f"BigQuery insert failed: {str(e)}", "warning")
            return False

    def fetch_secret(self, secret_id: str, version: str = "latest") -> str:
        """
        Fetch a secret value from Secret Manager.
        Args:
            secret_id: Secret resource name (projects/*/secrets/*)
            version: Secret version (default: latest)
        Returns:
            Secret payload as string, or empty string if not found
        """
        if not self.secret_manager_client:
            self.log_activity("Secret Manager client not available", "warning")
            return ""
        try:
            name = f"{secret_id}/versions/{version}"
            response = self.secret_manager_client.access_secret_version(request={"name": name})
            secret = response.payload.data.decode("UTF-8")
            self.log_activity(f"Fetched secret: {secret_id}")
            return secret
        except Exception as e:
            self.log_activity(f"Failed to fetch secret {secret_id}: {str(e)}", "warning")
            return ""

    def export_custom_metric(self, metric_type: str, value: float, labels: dict = None):
        """
        Export a custom metric to Cloud Monitoring.
        Args:
            metric_type: Custom metric type (e.g., custom.googleapis.com/agent/scan_duration)
            value: Metric value
            labels: Optional dictionary of labels
        """
        if not self.monitoring_client:
            self.log_activity("Cloud Monitoring client not available", "warning")
            return False
        try:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            if not project_id:
                self.log_activity("GOOGLE_CLOUD_PROJECT not set - skipping metric export", "warning")
                return False
            
            series = monitoring_v3.TimeSeries()
            series.metric.type = metric_type
            if labels:
                series.metric.labels.update(labels)
            series.resource.type = "global"
            series.resource.labels["project_id"] = project_id
            
            point = monitoring_v3.Point()
            point.value.double_value = value
            
            from google.protobuf.timestamp_pb2 import Timestamp
            from google.cloud.monitoring_v3.types import TimeInterval
            
            # Create timestamp properly with error handling
            try:
                current_time = datetime.now(UTC)
                timestamp = Timestamp()
                timestamp.FromDatetime(current_time)
                
                # Validate timestamp was created successfully
                if not hasattr(timestamp, 'seconds') or timestamp.seconds is None:
                    self.log_activity(f"Failed to create valid timestamp for metric {metric_type}", "warning")
                    return False
                
                interval = TimeInterval()
                interval.end_time = timestamp  # Direct assignment
                point.interval = interval  # Direct assignment
                series.points = [point]
                
                self.monitoring_client.create_time_series(name=f"projects/{project_id}", time_series=[series])
                self.log_activity(f"Exported custom metric: {metric_type}={value}")
                return True
                
            except Exception as timestamp_error:
                self.log_activity(f"Timestamp creation failed for metric {metric_type}: {str(timestamp_error)}", "warning")
                return False
                
        except Exception as e:
            self.log_activity(f"Failed to export custom metric {metric_type}: {str(e)}", "warning")
            return False

    # Cloud Function trigger template (for reference)
    # def cloud_function_entrypoint(request):
    #     """
    #     Cloud Function HTTP trigger for this agent.
    #     """
    #     # Parse request, call self.process(), return response
    #     pass 