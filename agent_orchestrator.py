"""
Privacy Guardian Agents - Main Orchestrator
Built with Google Cloud Agent Development Kit (ADK)

This orchestrator coordinates the multi-agent privacy enforcement system:
- PrivacyScanAgent: Initial code scanning
- GeminiAnalysisAgent: AI-powered analysis
- ComplianceAgent: Regulatory mapping
- FixSuggestionAgent: Code fix suggestions
- ReportAgent: Report generation
"""

import asyncio
import logging
import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import json
import sys

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.privacy_scan_agent import PrivacyScanAgent
from agents.gemini_analysis_agent import GeminiAnalysisAgent
from agents.compliance_agent import ComplianceAgent
from agents.fix_suggestion_agent import FixSuggestionAgent
from agents.report_agent import ReportAgent
from agents.base_agent import AgentEvent, ScanResult

class PrivacyGuardianOrchestrator:
    """Main orchestrator for Privacy Guardian Agents using ADK patterns"""
    
    def __init__(self):
        self.agents = {}
        self.event_history = []
        self.correlation_ids = {}
        self.logger = self._setup_logging()
        self._initialize_agents()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the orchestrator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger("privacy_guardian_orchestrator")
    
    def _initialize_agents(self):
        """Initialize all privacy guardian agents"""
        self.logger.info("🤖 Initializing Privacy Guardian Agents...")
        
        # Initialize agents
        self.agents['privacy_scan'] = PrivacyScanAgent()
        self.agents['gemini_analysis'] = GeminiAnalysisAgent()
        self.agents['compliance'] = ComplianceAgent()
        self.agents['fix_suggestion'] = FixSuggestionAgent()
        self.agents['report'] = ReportAgent()
        
        self.logger.info(f"✅ Initialized {len(self.agents)} agents")
        
        # Log agent status
        for agent_id, agent in self.agents.items():
            self.logger.info(f"  - {agent.agent_name} ({agent_id})")
    
    async def run_privacy_scan(self, project_path: str = ".", enable_ai: bool = True) -> Dict[str, Any]:
        """Run the complete privacy scanning pipeline using event-based architecture"""
        correlation_id = str(uuid.uuid4())
        self.correlation_ids[correlation_id] = {
            "start_time": datetime.now(UTC),
            "project_path": project_path,
            "enable_ai": enable_ai
        }
        
        self.logger.info(f"🚀 Starting Privacy Guardian scan (ID: {correlation_id})")
        self.logger.info(f"📁 Project path: {project_path}")
        self.logger.info(f"🤖 AI enabled: {enable_ai}")
        
        try:
            # Step 1: Initial Privacy Scan - emits FindingsReady event
            self.logger.info("🕵️ Step 1: Running PrivacyScanAgent...")
            scan_results = await self._run_privacy_scan_agent(project_path, correlation_id)
            
            if not scan_results:
                self.logger.info("✅ No violations found - scan complete")
                return await self._generate_final_report([], correlation_id)
            
            # Step 2: AI Analysis - listens for FindingsReady, emits AIEnhancedFindings
            if enable_ai:
                self.logger.info("🤖 Step 2: Running GeminiAnalysisAgent...")
                enhanced_results = await self._run_gemini_analysis_agent(scan_results, correlation_id)
            else:
                enhanced_results = scan_results
            
            # Step 3: Compliance Analysis - listens for AIEnhancedFindings, emits ComplianceAnalysisCompleted
            self.logger.info("🧑‍⚖️ Step 3: Running ComplianceAgent...")
            compliance_report = await self._run_compliance_agent(enhanced_results, correlation_id)
            
            # Step 4: Fix Suggestions - listens for ComplianceAnalysisCompleted, emits FixSuggestionsCompleted
            self.logger.info("🛠️ Step 4: Running FixSuggestionAgent...")
            fix_suggestions = await self._run_fix_suggestion_agent(enhanced_results, compliance_report, correlation_id)
            
            # Step 5: Report Generation - listens for FixSuggestionsCompleted, emits ReportGenerated
            self.logger.info("📋 Step 5: Running ReportAgent...")
            final_report = await self._run_report_agent(enhanced_results, compliance_report, fix_suggestions, correlation_id)
            
            # Log completion
            end_time = datetime.now(UTC)
            duration = (end_time - self.correlation_ids[correlation_id]["start_time"]).total_seconds()
            self.logger.info(f"✅ Privacy Guardian scan completed in {duration:.2f} seconds")
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"❌ Privacy Guardian scan failed: {str(e)}")
            return {
                "error": str(e),
                "correlation_id": correlation_id,
                "status": "failed"
            }
    
    async def _run_privacy_scan_agent(self, project_path: str, correlation_id: str) -> List[ScanResult]:
        """Run the privacy scan agent - emits FindingsReady event"""
        agent = self.agents['privacy_scan']
        
        input_data = {
            "project_path": project_path,
            "correlation_id": correlation_id
        }
        
        results = await agent.process(input_data)
        
        # Capture events
        self._capture_agent_events(agent, correlation_id)
        
        self.logger.info(f"🕵️ PrivacyScanAgent found {len(results)} violations - emitted FindingsReady event")
        return results
    
    async def _run_gemini_analysis_agent(self, scan_results: List[ScanResult], correlation_id: str) -> List[ScanResult]:
        """Run the Gemini analysis agent - listens for FindingsReady, emits AIEnhancedFindings"""
        agent = self.agents['gemini_analysis']
        
        # Convert ScanResult objects to dict for event passing
        scan_results_dict = [self._result_to_dict(result) for result in scan_results]
        
        input_data = {
            "scan_results": scan_results_dict,
            "correlation_id": correlation_id
        }
        
        results = await agent.process(input_data)
        
        # Capture events
        self._capture_agent_events(agent, correlation_id)
        
        original_count = len(scan_results)
        enhanced_count = len(results)
        new_violations = enhanced_count - original_count
        
        self.logger.info(f"🤖 GeminiAnalysisAgent enhanced {original_count} violations, found {new_violations} new violations - emitted AIEnhancedFindings event")
        return results
    
    async def _run_compliance_agent(self, enhanced_results: List[ScanResult], correlation_id: str) -> Dict[str, Any]:
        """Run the compliance agent - listens for AIEnhancedFindings, emits ComplianceAnalysisCompleted"""
        agent = self.agents['compliance']
        
        # Convert ScanResult objects to dict for event passing
        enhanced_results_dict = [self._result_to_dict(result) for result in enhanced_results]
        
        input_data = {
            "enhanced_results": enhanced_results_dict,
            "correlation_id": correlation_id
        }
        
        compliance_report = await agent.process(input_data)
        
        # Capture events
        self._capture_agent_events(agent, correlation_id)
        
        # Count regulations affected
        regulations = set()
        for result in enhanced_results:
            for reg in result.regulation_reference.split(', '):
                if reg.strip():
                    regulations.add(reg.strip())
        
        self.logger.info(f"🧑‍⚖️ ComplianceAgent analyzed {len(enhanced_results)} violations across {len(regulations)} regulations - emitted ComplianceAnalysisCompleted event")
        return compliance_report
    
    async def _run_fix_suggestion_agent(self, enhanced_results: List[ScanResult], compliance_report: Dict[str, Any], correlation_id: str) -> Dict[str, Any]:
        """Run the fix suggestion agent - listens for ComplianceAnalysisCompleted, emits FixSuggestionsCompleted"""
        agent = self.agents['fix_suggestion']
        
        # Convert ScanResult objects to dict for event passing
        enhanced_results_dict = [self._result_to_dict(result) for result in enhanced_results]
        
        input_data = {
            "enhanced_results": enhanced_results_dict,
            "compliance_report": compliance_report,
            "correlation_id": correlation_id
        }
        
        fix_suggestions = await agent.process(input_data)
        
        # Capture events
        self._capture_agent_events(agent, correlation_id)
        
        self.logger.info(f"🛠️ FixSuggestionAgent generated fix suggestions - emitted FixSuggestionsCompleted event")
        return fix_suggestions
    
    async def _run_report_agent(self, enhanced_results: List[ScanResult], compliance_report: Dict[str, Any], fix_suggestions: Dict[str, Any], correlation_id: str) -> Dict[str, Any]:
        """Run the report agent - listens for FixSuggestionsCompleted, emits ReportGenerated"""
        agent = self.agents['report']
        
        # Convert ScanResult objects to dict for event passing
        enhanced_results_dict = [self._result_to_dict(result) for result in enhanced_results]
        
        input_data = {
            "enhanced_results": enhanced_results_dict,
            "compliance_report": compliance_report,
            "fix_suggestions": fix_suggestions,
            "correlation_id": correlation_id
        }
        
        final_report = await agent.process(input_data)
        
        # Capture events
        self._capture_agent_events(agent, correlation_id)
        
        self.logger.info(f"📋 ReportAgent generated comprehensive report - emitted ReportGenerated event")
        return final_report
    
    def _capture_agent_events(self, agent, correlation_id: str):
        """Capture events from an agent"""
        for event in agent.events_published:
            if event.correlation_id == correlation_id:
                self.event_history.append(event)
    
    async def _generate_final_report(self, scan_results: List[ScanResult], correlation_id: str) -> Dict[str, Any]:
        """Generate final report even if no violations found"""
        return {
            "correlation_id": correlation_id,
            "status": "completed",
            "total_violations": len(scan_results),
            "agents_used": list(self.agents.keys()),
            "scan_results": [self._result_to_dict(r) for r in scan_results],
            "event_summary": self._generate_event_summary(correlation_id),
            "timestamp": datetime.now(UTC).isoformat()
        }
    
    def _result_to_dict(self, result: ScanResult) -> Dict[str, Any]:
        """Convert ScanResult to dictionary"""
        return {
            "file_path": result.file_path,
            "line_number": result.line_number,
            "violation_type": result.violation_type,
            "description": result.description,
            "severity": result.severity,
            "fix_suggestion": result.fix_suggestion,
            "regulation_reference": result.regulation_reference,
            "agent_id": result.agent_id,
            "timestamp": result.timestamp.isoformat()
        }
    
    def _generate_event_summary(self, correlation_id: str) -> Dict[str, Any]:
        """Generate summary of events for correlation ID"""
        events = [e for e in self.event_history if e.correlation_id == correlation_id]
        
        event_types = {}
        agent_activity = {}
        
        for event in events:
            # Count event types
            if event.event_type not in event_types:
                event_types[event.event_type] = 0
            event_types[event.event_type] += 1
            
            # Count agent activity
            if event.agent_id not in agent_activity:
                agent_activity[event.agent_id] = 0
            agent_activity[event.agent_id] += 1
        
        return {
            "total_events": len(events),
            "event_types": event_types,
            "agent_activity": agent_activity
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = agent.get_agent_status()
        return status
    
    def get_event_history(self, correlation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get event history, optionally filtered by correlation ID"""
        events = self.event_history
        if correlation_id:
            events = [e for e in events if e.correlation_id == correlation_id]
        
        return [
            {
                "event_type": e.event_type,
                "agent_id": e.agent_id,
                "timestamp": e.timestamp.isoformat(),
                "data": e.data,
                "correlation_id": e.correlation_id
            }
            for e in events
        ]

# Main execution function
async def main():
    """Main function for running Privacy Guardian Agents"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Privacy Guardian Agents - Multi-Agent Privacy Enforcement")
    parser.add_argument("--project-path", default=".", help="Path to project to scan")
    parser.add_argument("--disable-ai", action="store_true", help="Disable AI analysis")
    parser.add_argument("--agent-status", action="store_true", help="Show agent status")
    parser.add_argument("--event-history", help="Show event history for correlation ID")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = PrivacyGuardianOrchestrator()
    
    if args.agent_status:
        # Show agent status
        status = orchestrator.get_agent_status()
        print("🤖 Agent Status:")
        for agent_id, agent_status in status.items():
            print(f"  {agent_status['agent_name']}: {agent_status['status']}")
        return
    
    if args.event_history:
        # Show event history
        events = orchestrator.get_event_history(args.event_history)
        print(f"📋 Event History for {args.event_history}:")
        for event in events:
            print(f"  {event['timestamp']} - {event['agent_id']}: {event['event_type']}")
        return
    
    # Run privacy scan
    print("🚀 Privacy Guardian Agents - Starting Scan")
    print("=" * 50)
    
    result = await orchestrator.run_privacy_scan(
        project_path=args.project_path,
        enable_ai=not args.disable_ai
    )
    
    if "error" in result:
        print(f"❌ Scan failed: {result['error']}")
        return
    
    print("\n" + "=" * 50)
    print("✅ Privacy Guardian Scan Complete!")
    
    # Extract total violations from the correct location in the report
    total_violations = 0
    if 'metadata' in result and 'total_violations' in result['metadata']:
        total_violations = result['metadata']['total_violations']
    elif 'total_violations' in result:
        total_violations = result['total_violations']
    
    print(f"📊 Total Violations: {total_violations}")
    print(f"🆔 Correlation ID: {result.get('correlation_id', 'N/A')}")
    
    # Extract additional report information
    if 'metadata' in result:
        metadata = result['metadata']
        if 'agents_used' in metadata:
            print(f"🤖 Agents Used: {', '.join(metadata['agents_used'])}")
        if 'gemini_enhanced' in metadata:
            print(f"🤖 AI Enhanced: {metadata['gemini_enhanced']}")
    
    if 'executive_summary' in result:
        summary = result['executive_summary']
        if 'compliance_score' in summary:
            print(f"🎯 Compliance Score: {summary['compliance_score']}%")
        if 'risk_level' in summary:
            print(f"⚠️ Risk Level: {summary['risk_level']}")
    
    if 'pdf_path' in result:
        print(f"📄 PDF Report: {result['pdf_path']}")
    
    if 'cloud_url' in result and result['cloud_url']:
        print(f"☁️ Cloud Report: {result['cloud_url']}")
    
    # Show storage location if available
    if 'storage_location' in result:
        print(f"💾 Report Stored: {result['storage_location']}")

if __name__ == "__main__":
    asyncio.run(main()) 