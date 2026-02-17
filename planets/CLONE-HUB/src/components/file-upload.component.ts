
import { Component, output, signal } from '@angular/core';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  template: `
    <div 
      class="border-2 border-dashed border-slate-800 rounded-lg p-16 md:p-24 text-center transition-all duration-500 cursor-pointer group bg-black hover:border-fuchsia-500/50 hover:bg-[#050505]"
      (click)="fileInput.click()"
      (drop)="onDrop($event)"
      (dragover)="onDragOver($event)"
      (dragleave)="isDragging.set(false)"
      [class.border-fuchsia-500]="isDragging()"
      [class.bg-fuchsia-900/10]="isDragging()"
    >
      <input 
        #fileInput 
        type="file" 
        class="hidden" 
        accept=".txt,.md"
        (change)="onFileSelected($event)"
      >
      
      <div class="flex flex-col items-center gap-6 group-hover:-translate-y-2 transition-transform duration-500">
        <div class="p-6 bg-slate-900/50 border border-slate-800 rounded-full group-hover:border-fuchsia-500 group-hover:bg-fuchsia-900/20 transition-all duration-500 shadow-2xl">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 group-hover:text-fuchsia-400 transition-colors">
            <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path>
            <path d="M12 12v9"></path>
            <path d="m16 16-4-4-4 4"></path>
          </svg>
        </div>
        
        <div class="space-y-2">
          <h3 class="text-xl md:text-2xl font-bold text-slate-200 group-hover:text-white tracking-wide transition-colors">
            اسحب المخطوطة هنا
          </h3>
          <p class="text-xs text-slate-500 font-mono tracking-widest uppercase group-hover:text-fuchsia-400/70 transition-colors">
            أو انقر للاستعراض
          </p>
        </div>
      </div>
    </div>
  `
})
export class FileUploadComponent {
  fileContent = output<string>();
  isDragging = signal(false);

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(true);
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);
    if (event.dataTransfer?.files?.length) {
      this.processFile(event.dataTransfer.files[0]);
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.processFile(input.files[0]);
    }
  }

  private processFile(file: File) {
    if (file.type === 'text/plain' || file.name.endsWith('.txt') || file.name.endsWith('.md')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        this.fileContent.emit(text);
      };
      reader.readAsText(file);
    } else {
      alert('نقبل فقط الملفات النصية (TXT/MD) لضمان دقة التحليل.');
    }
  }
}
