
import { Component, inject, signal, computed, effect, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NexusEngineService } from './services/nexus-engine.service';
import { FileUploadComponent } from './components/file-upload.component';
import { DashboardComponent } from './components/dashboard.component';
import { BookMetadata, ProjectArchetype, ExpansionStrategy, ToneVoice, PageTarget } from './types';

type AppState = 'IDLE' | 'PROCESSING' | 'COMPLETED';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FileUploadComponent, DashboardComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {
  service = inject(NexusEngineService);
  
  // Simple State Machine
  state = signal<AppState>('IDLE');
  
  // Data
  rawText = signal<string>('');
  
  // Default Elite Metadata (Since we skipped the questionnaire)
  metadata: BookMetadata = {
    language: 'ar',
    userName: 'Elite Author',
    projectArchetype: ProjectArchetype.NONFICTION_AUTHORITY,
    pageTarget: PageTarget.MAINTAIN,
    expansionStrategy: ExpansionStrategy.NARRATIVE_ENRICHMENT,
    toneVoice: ToneVoice.AUTHORITATIVE,
    title: 'Project Nexus', // Will be updated from filename if possible
    author: 'Unknown',
    targetAudience: 'Elite',
    coverDescription: 'Minimalist, luxary, dark theme'
  };

  constructor() {
    // Auto-transition when complete
    effect(() => {
      const status = this.service.status();
      if (status.stage === 'complete' && this.state() === 'PROCESSING') {
          setTimeout(() => {
             this.state.set('COMPLETED');
          }, 2000);
      }
    }, { allowSignalWrites: true });
  }

  onFileUploaded(content: string) {
      if (!content) return;
      
      this.rawText.set(content);
      
      // 1. Immediate Transition to Dashboard
      this.state.set('PROCESSING');

      // 2. Start Engine after small UI delay
      setTimeout(() => {
        this.service.executeProtocol(this.rawText(), this.metadata);
      }, 100);
  }

  downloadPackage() {
      const pkg = this.service.finalPackage();
      if (!pkg || !pkg.zipBlob) return;
      const url = window.URL.createObjectURL(pkg.zipBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Nexus_Elite_Package.zip`;
      a.click();
  }
  
  reload() { 
    window.location.reload(); 
  }
}
