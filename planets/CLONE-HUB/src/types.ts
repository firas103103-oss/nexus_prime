
export type ChatRole = 'agent' | 'user' | 'system';

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  timestamp: Date;
  options?: { label: string; value: any; description?: string }[];
  inputType?: 'text' | 'file' | 'confirmation';
  attachmentName?: string;
}

export interface LogEntry {
  timestamp: Date;
  message: string;
  type: 'info' | 'success' | 'warn' | 'system';
}

export enum ProjectArchetype {
  FICTION_EPIC = 'FICTION_EPIC', 
  NONFICTION_AUTHORITY = 'NONFICTION_AUTHORITY', 
  ACADEMIC_THESIS = 'ACADEMIC_THESIS', 
  LEGAL_CODEX = 'LEGAL_CODEX', 
  PHILOSOPHICAL_TREATISE = 'PHILOSOPHICAL_TREATISE'
}

export enum PageTarget {
  MAINTAIN = 'Maintain Current Volume (±10%)',
  EXPAND_SLIGHTLY = 'Moderate Expansion (+30%)',
  MAXIMUM_DEPTH = 'Maximum Depth (Aim for 200k Words)'
}

export enum ExpansionStrategy {
  CONSERVATIVE = 'Conservative Polish',
  NARRATIVE_ENRICHMENT = 'Narrative Enrichment',
  ACADEMIC_EXPANSION = 'Academic/Contextual Expansion'
}

export enum ToneVoice {
  AUTHORITATIVE = 'Authoritative',
  SOCRATIC = 'Socratic',
  NARRATIVE_DRIVEN = 'Narrative Driven',
  ACADEMIC_RIGOR = 'Academic Rigor'
}

export interface BookMetadata {
  language: 'ar' | 'en' | 'de';
  userName: string;
  projectArchetype: ProjectArchetype;
  pageTarget: PageTarget;
  expansionStrategy: ExpansionStrategy;
  toneVoice: ToneVoice;
  title: string;
  author: string;
  targetAudience: string;
  coverDescription?: string;
}

export interface ProcessingStatus {
  stage: 'idle' | 'analyzing_bg' | 'auditing' | 'blueprint' | 'expansion' | 'visuals' | 'director' | 'analyst' | 'finalizing' | 'complete' | 'error';
  progress: number;
  message: string;
  agentName?: string;
}

export interface SocialPost {
  id: number;
  quote: string;
  imageBase64: string;
  caption: string;
}

export interface PublishingPackage {
  originalText: string;
  editedText: string;
  coverImageBase64: string;
  marketingVideoUrl: string;
  socialPosts: SocialPost[];
  reports: {
      marketAnalysis: string;
      strategicDeck: string;
      officialLetter: string;
  };
  zipBlob?: Blob;
}

export enum ChatStep {
  LANGUAGE_SELECT,
  UPLOAD_MANUSCRIPT, // Step 2: Upload First
  USER_NAME,
  PAGE_TARGET,       // Step 4: Page Target
  PROJECT_ARCHETYPE,
  EXPANSION_STRATEGY,
  TONE_CALIBRATION,
  BOOK_TITLE,
  BOOK_AUTHOR,
  VISUAL_BRIEF,
  CONFIRMATION,
  PROCESSING,
  COMPLETED,
  ERROR
}

export const AR_LABELS: Record<string, string> = {
  [ProjectArchetype.FICTION_EPIC]: 'رواية ملحمية (سرد قصصي)',
  [ProjectArchetype.NONFICTION_AUTHORITY]: 'مرجع تخصصي (سلطة معرفية)',
  [ProjectArchetype.ACADEMIC_THESIS]: 'أطروحة أكاديمية',
  [ProjectArchetype.LEGAL_CODEX]: 'مدونة قانونية',
  [ProjectArchetype.PHILOSOPHICAL_TREATISE]: 'رسالة فلسفية',

  [PageTarget.MAINTAIN]: 'الحفاظ على الحجم الحالي (±10%)',
  [PageTarget.EXPAND_SLIGHTLY]: 'توسع متوسط (+30%)',
  [PageTarget.MAXIMUM_DEPTH]: 'العمق الأقصى (هدف 200 ألف كلمة)',

  [ExpansionStrategy.CONSERVATIVE]: 'تحسين لغوي وصياغي فقط',
  [ExpansionStrategy.NARRATIVE_ENRICHMENT]: 'إثراء سردي وبلاغي',
  [ExpansionStrategy.ACADEMIC_EXPANSION]: 'توسع في الشرح والسياق',

  [ToneVoice.AUTHORITATIVE]: 'نبرة سلطوية (الخبير)',
  [ToneVoice.SOCRATIC]: 'نبرة سقراطية (تساؤل)',
  [ToneVoice.NARRATIVE_DRIVEN]: 'نبرة روائية (سرد)',
  [ToneVoice.ACADEMIC_RIGOR]: 'نبرة أكاديمية (توثيق)'
};
