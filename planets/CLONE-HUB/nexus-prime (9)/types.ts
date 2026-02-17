
export interface NexusReport {
  title: string;
  professional_verdict: string;
  executive_summary: string;
  deep_analysis_markdown: string;
}

export interface NexusState {
  visual_mode: 'VOID_IDLE' | 'GRAVITY_WELL_ACTIVE' | 'PANORAMIC_DASHBOARD' | 'INTRO_MODE';
  animation_trigger: string | null;
  hex_accent: string;
  ui_message_overlay: string;
}

export type AgentType = 'VISUAL_CORE' | 'SECURITY_OPS' | 'DATA_MINER' | 'EXECUTIVE' | 'THINKER';

export interface DialoguePacket {
  agent: AgentType;
  text: string;
}

export interface AIResponse {
  ux_orchestration: {
    visual_state: NexusState['visual_mode'];
    hex_accent: string;
    ui_message_overlay: string;
  };
  hive_mind_dialogue: DialoguePacket[];
  final_voice_script: string;
  data_payload: NexusReport;
}
