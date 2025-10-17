import streamlit as st
import time
from typing import Dict, Any, List, Optional
import threading
from datetime import datetime


class ProgressTracker:
    """Real-time progress tracking for workflow execution."""
    
    def __init__(self):
        self.current_stage = None
        self.stages_completed = 0
        self.total_stages = 5
        self.stage_details = {}
        self.start_time = None
        self.is_running = False
        
    def start_tracking(self, stages: List[str]) -> None:
        """Start progress tracking."""
        self.total_stages = len(stages)
        self.stages_completed = 0
        self.current_stage = None
        self.stage_details = {}
        self.start_time = datetime.now()
        self.is_running = True
        
        # Initialize stage details
        for i, stage in enumerate(stages):
            self.stage_details[stage] = {
                'order': i + 1,
                'status': 'pending',
                'start_time': None,
                'end_time': None,
                'duration': 0,
                'progress': 0
            }
    
    def update_stage(self, stage_name: str, status: str, progress: int = 0) -> None:
        """Update stage progress."""
        if stage_name in self.stage_details:
            stage_info = self.stage_details[stage_name]
            
            if status == 'running' and stage_info['start_time'] is None:
                stage_info['start_time'] = datetime.now()
                self.current_stage = stage_name
                
            elif status in ['completed', 'success', 'failed']:
                stage_info['end_time'] = datetime.now()
                if stage_info['start_time']:
                    duration = (stage_info['end_time'] - stage_info['start_time']).total_seconds()
                    stage_info['duration'] = duration
                
                if status in ['completed', 'success']:
                    self.stages_completed += 1
                    progress = 100
                
                self.current_stage = None
            
            stage_info['status'] = status
            stage_info['progress'] = progress
    
    def finish_tracking(self) -> None:
        """Finish progress tracking."""
        self.is_running = False
        self.current_stage = None
    
    def get_overall_progress(self) -> float:
        """Get overall progress percentage."""
        if self.total_stages == 0:
            return 0
        
        completed_progress = self.stages_completed * 100
        
        # Add current stage progress
        if self.current_stage and self.current_stage in self.stage_details:
            current_progress = self.stage_details[self.current_stage]['progress']
            completed_progress += current_progress
        
        return min(100, completed_progress / self.total_stages)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        return (datetime.now() - self.start_time).total_seconds()


def show_progress_tracker(tracker: ProgressTracker) -> None:
    """Display real-time progress tracking interface."""
    
    if not tracker.is_running:
        return
    
    st.subheader("🔄 Workflow Progress")
    
    # Overall progress
    overall_progress = tracker.get_overall_progress()
    elapsed_time = tracker.get_elapsed_time()
    
    # Progress bar
    progress_bar = st.progress(overall_progress / 100)
    
    # Status info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Progress", f"{overall_progress:.1f}%")
    
    with col2:
        st.metric("Elapsed Time", f"{elapsed_time:.1f}s")
    
    with col3:
        st.metric("Stages Completed", f"{tracker.stages_completed}/{tracker.total_stages}")
    
    # Current stage info
    if tracker.current_stage:
        current_info = tracker.stage_details[tracker.current_stage]
        st.info(f"🔄 Currently running: **{tracker.current_stage}** ({current_info['progress']}%)")
    
    # Stage details
    st.subheader("📋 Stage Details")
    
    for stage_name, details in tracker.stage_details.items():
        status = details['status']
        progress = details['progress']
        duration = details['duration']
        order = details['order']
        
        # Status icon
        if status == 'completed' or status == 'success':
            status_icon = "✅"
            status_color = "green"
        elif status == 'running':
            status_icon = "🔄"
            status_color = "blue"
        elif status == 'failed':
            status_icon = "❌"
            status_color = "red"
        else:
            status_icon = "⏳"
            status_color = "gray"
        
        # Create expandable stage info
        with st.expander(f"{status_icon} Stage {order}: {stage_name} ({progress}%)", expanded=(status == 'running')):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.write(f"**Status:** {status.title()}")
            
            with col_b:
                if duration > 0:
                    st.write(f"**Duration:** {duration:.1f}s")
                else:
                    st.write("**Duration:** -")
            
            with col_c:
                st.write(f"**Progress:** {progress}%")
            
            # Progress bar for individual stage
            if status == 'running':
                st.progress(progress / 100)


def show_workflow_animation() -> None:
    """Show animated workflow visualization."""
    
    st.subheader("🎬 Workflow Animation")
    
    # Create animated workflow diagram
    stages = [
        "📄 Policy Document",
        "🔍 PolicyEvaluator", 
        "📋 RequirementsCapture",
        "❓ QuestionGenerator",
        "✅ ValidationAgent",
        "📦 ConsolidationAgent",
        "📊 Results"
    ]
    
    # Simple animation using columns
    cols = st.columns(len(stages))
    
    for i, (col, stage) in enumerate(zip(cols, stages)):
        with col:
            # Determine if this stage is active, completed, or pending
            if i < 2:  # Completed stages
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: #d4edda; 
                           border: 2px solid #28a745; border-radius: 10px; margin: 5px;">
                    <div style="font-size: 24px;">{stage.split()[0]}</div>
                    <div style="font-size: 12px; font-weight: bold;">{' '.join(stage.split()[1:])}</div>
                    <div style="color: #28a745;">✅ Complete</div>
                </div>
                """, unsafe_allow_html=True)
            elif i == 2:  # Current stage
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: #cce5ff; 
                           border: 2px solid #007bff; border-radius: 10px; margin: 5px; 
                           animation: pulse 2s infinite;">
                    <div style="font-size: 24px;">{stage.split()[0]}</div>
                    <div style="font-size: 12px; font-weight: bold;">{' '.join(stage.split()[1:])}</div>
                    <div style="color: #007bff;">🔄 Running</div>
                </div>
                """, unsafe_allow_html=True)
            else:  # Pending stages
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: #f8f9fa; 
                           border: 2px solid #6c757d; border-radius: 10px; margin: 5px;">
                    <div style="font-size: 24px;">{stage.split()[0]}</div>
                    <div style="font-size: 12px; font-weight: bold;">{' '.join(stage.split()[1:])}</div>
                    <div style="color: #6c757d;">⏳ Pending</div>
                </div>
                """, unsafe_allow_html=True)


def create_progress_placeholder() -> Dict[str, Any]:
    """Create placeholders for progress tracking UI elements."""
    
    placeholders = {
        'progress_container': st.empty(),
        'status_container': st.empty(),
        'stage_container': st.empty(),
        'animation_container': st.empty()
    }
    
    return placeholders


def update_progress_display(placeholders: Dict[str, Any], tracker: ProgressTracker) -> None:
    """Update progress display in placeholders."""
    
    with placeholders['progress_container']:
        if tracker.is_running:
            show_progress_tracker(tracker)
    
    with placeholders['animation_container']:
        if tracker.is_running:
            show_workflow_animation()


# Demo progress simulation
def simulate_workflow_progress(tracker: ProgressTracker, placeholders: Dict[str, Any]) -> None:
    """Simulate workflow progress for demonstration."""
    
    stages = [
        "PolicyEvaluator",
        "RequirementsCapture", 
        "QuestionGenerator",
        "ValidationAgent",
        "ConsolidationAgent"
    ]
    
    tracker.start_tracking(stages)
    
    for stage in stages:
        # Start stage
        tracker.update_stage(stage, 'running', 0)
        update_progress_display(placeholders, tracker)
        
        # Simulate progress
        for progress in range(0, 101, 20):
            time.sleep(0.5)  # Simulate work
            tracker.update_stage(stage, 'running', progress)
            update_progress_display(placeholders, tracker)
        
        # Complete stage
        tracker.update_stage(stage, 'completed', 100)
        update_progress_display(placeholders, tracker)
        time.sleep(0.5)
    
    tracker.finish_tracking()
    update_progress_display(placeholders, tracker)


# CSS for animations
def add_progress_css() -> None:
    """Add CSS for progress animations."""
    
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .progress-stage {
        animation: fadeIn 0.5s ease-in;
    }
    
    .current-stage {
        animation: pulse 2s infinite;
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.5);
    }
    
    .completed-stage {
        animation: fadeIn 0.5s ease-in;
        box-shadow: 0 0 10px rgba(40, 167, 69, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
