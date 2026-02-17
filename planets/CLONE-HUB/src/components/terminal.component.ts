
import { Component, input, effect, ElementRef, ViewChild, computed } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-terminal',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="w-full h-[450px] bg-[#050505] border border-white/10 rounded-sm overflow-hidden font-mono text-sm relative shadow-2xl group">
      <!-- Header -->
      <div class="bg-black p-3 border-b border-white/5 flex justify-between items-center text-[9px] text-slate-600 select-none">
        <div class="flex gap-2 opacity-50">
          <span class="w-2 h-2 rounded-full bg-slate-700"></span>
          <span class="w-2 h-2 rounded-full bg-slate-700"></span>
          <span class="w-2 h-2 rounded-full bg-slate-700"></span>
        </div>
        <div class="tracking-[0.3em] text-fuchsia-500/40 uppercase">Secure Connection :: Mr X OS</div>
      </div>

      <!-- Matrix Bg -->
      <div class="absolute inset-0 opacity-[0.02] pointer-events-none" style="background-image: linear-gradient(0deg, transparent 24%, rgba(255, 255, 255, .5) 25%, rgba(255, 255, 255, .5) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, .5) 75%, rgba(255, 255, 255, .5) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(255, 255, 255, .5) 25%, rgba(255, 255, 255, .5) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, .5) 75%, rgba(255, 255, 255, .5) 76%, transparent 77%, transparent); background-size: 40px 40px;"></div>

      <!-- Content -->
      <div #scrollContainer class="p-8 h-full overflow-y-auto pb-12 text-violet-300 font-light scrollbar-hide">
        <div class="mb-8 text-cyan-600/40 whitespace-pre text-[6px] md:text-[8px] leading-tight select-none opacity-50">
  __  __ _____    __   __   ____   _____ 
 |  \/  |  __ \   \ \ / /  / __ \ / ____|
 | \  / | |__) |   \ V /  | |  | | (___  
 | |\/| |  _  /     > <   | |  | |\___ \ 
 | |  | | | \ \    / . \  | |__| |____) |
 |_|  |_|_|  \_\  /_/ \_\  \____/|_____/ 
        SYSTEM V4.0 // INITIALIZED
        </div>

        @for (log of logsInput(); track $index) {
          <div class="mb-2 flex gap-4 animate-fade-in-left border-l border-white/5 pl-4 group-hover:border-fuchsia-500/20 transition-colors duration-500">
            <span class="text-cyan-800 text-[10px] pt-0.5">➜</span>
            <span class="typing-effect text-xs md:text-sm tracking-wide text-slate-400 group-hover:text-slate-200 transition-colors">{{ log }}</span>
          </div>
        }
        
        @if (isProcessingInput()) {
           <div class="mb-1 flex gap-4 animate-pulse mt-6 pl-4">
            <span class="text-fuchsia-800">➜</span>
            <span class="text-fuchsia-600 tracking-widest text-xs">PROCESSING STREAM [{{ hexId }}]...</span>
          </div>
        }
      </div>
    </div>
  `,
  styles: [`
    .animate-fade-in-left { animation: fadeInLeft 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
    @keyframes fadeInLeft { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
    
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #555; }
  `]
})
export class TerminalInterfaceComponent {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  
  logsInput = input<string[]>([]);
  isProcessingInput = input<boolean>(false);
  
  hexId = '0x' + Math.floor(Math.random()*16777215).toString(16).toUpperCase();

  constructor() {
    effect(() => {
      this.logsInput(); 
      this.scrollToBottom();
    });
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    }, 50);
  }
}
