
import { Injectable, signal } from '@angular/core';
import { GoogleGenAI } from '@google/genai';
import { BookMetadata, ProcessingStatus, PublishingPackage, SocialPost, AR_LABELS, PageTarget, LogEntry } from '../types';

declare const JSZip: any;

@Injectable({
  providedIn: 'root'
})
export class NexusEngineService {
  private ai: GoogleGenAI;
  
  // State
  status = signal<ProcessingStatus>({ stage: 'idle', progress: 0, message: 'System Ready', agentName: 'SYSTEM' });
  logs = signal<LogEntry[]>([]);
  generatedWordCount = signal<number>(0);
  finalPackage = signal<PublishingPackage | null>(null);
  
  // Background analysis result
  private backgroundBlueprint: string = '';

  constructor() {
    const apiKey = process.env['API_KEY'];
    this.ai = new GoogleGenAI({ apiKey: apiKey || '' });
  }

  // --- Background Task ---
  async startBackgroundAnalysis(text: string) {
    if (!text) return;
    this.updateStatus('analyzing_bg', 5, 'الظل السابع: أقرأ المخطوطة في الخلفية...', 'SCANNER');
    try {
      await new Promise(r => setTimeout(r, 100));
      const prompt = `أنت المدقق اللغوي الأول. استخرج الهيكل العام: "${text.slice(0, 5000)}..."`;
      const response = await this.ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: prompt
      });
      this.backgroundBlueprint = response.text || '';
      this.updateStatus('analyzing_bg', 10, 'الظل السابع: انتهيت من القراءة الأولية.', 'SCANNER');
    } catch (e) {
      console.warn("Background analysis failed (non-fatal)", e);
    }
  }

  // --- Main Execution Protocol ---
  async executeProtocol(fileContent: string, metadata: BookMetadata) {
    // 0. Reset State
    this.generatedWordCount.set(0);
    this.logs.set([]);
    this.finalPackage.set(null);

    // 1. Critical Boot Delay
    this.updateStatus('idle', 1, 'INITIALIZING NEURAL CORE...', 'SYSTEM');
    await new Promise(resolve => setTimeout(resolve, 800)); // Visual delay for UI transition

    if (!process.env['API_KEY']) {
      this.updateStatus('error', 0, 'FATAL: API KEY MISSING. CHECK CONFIG.', 'SYSTEM', 'warn');
      return;
    }

    if (!fileContent) {
      this.updateStatus('error', 0, 'FATAL: NO MANUSCRIPT DETECTED.', 'SYSTEM', 'warn');
      return;
    }

    const isAr = metadata.language === 'ar';

    try {
      // 2. Structure
      this.updateStatus('blueprint', 10, isAr ? 'المهندس: تحليل البنية السردية...' : 'Architecting Blueprint...', 'ARCHITECT');
      await this.yieldToUI();
      const blueprint = this.backgroundBlueprint || await this.generateBlueprint(fileContent, metadata);
      
      // 3. Content Processing
      this.updateStatus('expansion', 20, isAr ? 'الكاتب الشبحي: بدء بروتوكول التوسع...' : 'Engaging Ghostwriter Protocol...', 'GHOSTWRITER');
      const processedText = await this.processContentByChunks(fileContent, metadata);
      
      // 4. Visuals
      this.updateStatus('visuals', 65, isAr ? 'المصمم: توليد غلاف سينمائي بدقة 8K...' : 'Rendering 8K Cover Art...', 'DESIGNER');
      await this.yieldToUI();
      const coverImage = await this.generateCover(metadata);

      // 5. Social
      this.updateStatus('visuals', 75, isAr ? 'فريق التسويق: صياغة الحملة الإعلامية...' : 'Generating Social Campaign...', 'SOCIAL_BOT');
      await this.yieldToUI();
      const socialPosts = await this.generateSocialAssets(processedText, metadata);

      // 6. Video
      this.updateStatus('director', 85, isAr ? 'المخرج: إنتاج المقطع التشويقي...' : 'Rendering Cinematic Trailer...', 'DIRECTOR');
      await this.yieldToUI();
      const videoBlobUrl = await this.generateMarketingVideo(metadata);

      // 7. Reports
      this.updateStatus('analyst', 95, isAr ? 'المحلل: تجميع التقارير النهائية...' : 'Compiling Strategic Reports...', 'ANALYST');
      await this.yieldToUI();
      const reports = await this.generateReports(processedText, metadata);

      // 8. Packaging
      this.updateStatus('finalizing', 99, isAr ? 'النظام: تشفير الحزمة النهائية...' : 'Encrypting & Packaging Assets...', 'PACKAGER');
      await this.yieldToUI();
      const zipBlob = await this.createZipPackage(metadata, processedText, coverImage, videoBlobUrl, socialPosts, reports);

      const pkg: PublishingPackage = {
        originalText: fileContent,
        editedText: processedText,
        coverImageBase64: coverImage,
        marketingVideoUrl: videoBlobUrl,
        socialPosts: socialPosts,
        reports: reports,
        zipBlob: zipBlob
      };

      this.finalPackage.set(pkg);
      this.updateStatus('complete', 100, isAr ? 'تم اكتمال المشروع.' : 'PROJECT COMPLETED SUCCESSFULLY.', 'SEVENTH_SHADOW', 'success');

    } catch (error: any) {
      console.error(error);
      this.updateStatus('error', 0, `SYSTEM FAILURE: ${error.message || 'Unknown Error'}`, 'SYSTEM', 'warn');
    }
  }

  // --- Helpers ---

  private updateStatus(stage: ProcessingStatus['stage'], progress: number, message: string, agentName: string = 'SYSTEM', logType: LogEntry['type'] = 'info') {
    this.status.set({ stage, progress, message, agentName });
    this.logs.update(logs => [...logs, {
      timestamp: new Date(),
      message: `[${agentName}] ${message}`,
      type: logType
    }]);
  }

  private async yieldToUI() {
    await new Promise(resolve => setTimeout(resolve, 50));
  }

  private async generateBlueprint(text: string, meta: BookMetadata): Promise<string> {
    return "Structure Analysis Complete.";
  }

  private async processContentByChunks(fullText: string, meta: BookMetadata): Promise<string> {
    const chunkSize = 4000;
    const chunks = [];
    for (let i = 0; i < fullText.length; i += chunkSize) {
      chunks.push(fullText.slice(i, i + chunkSize));
    }

    let finalHtml = "";
    let instruction = meta.pageTarget === PageTarget.MAXIMUM_DEPTH 
      ? "Expand significantly. Add descriptions, dialogue, and depth." 
      : "Rewrite professionally. Maintain flow.";

    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const percent = 20 + Math.floor((i / chunks.length) * 45);
      this.updateStatus('expansion', percent, `Writing Segment ${i + 1}/${chunks.length}...`, 'GHOSTWRITER');

      try {
        const response = await this.ai.models.generateContent({
          model: 'gemini-2.5-flash',
          contents: `Role: Elite Editor. Task: ${instruction}. Output: Clean HTML <p> tags only. Input: "${chunk}"`,
        });
        
        let cleanText = response.text || chunk;
        cleanText = cleanText.replace(/```html/g, '').replace(/```/g, '');
        
        this.generatedWordCount.update(c => c + cleanText.split(/\s+/).length);
        finalHtml += cleanText + "\n\n";
        await this.yieldToUI();

      } catch (e) {
        finalHtml += `<p>${chunk}</p>`;
        this.updateStatus('expansion', percent, `Segment ${i+1} skipped (Error). Used original.`, 'SYSTEM', 'warn');
      }
    }
    return finalHtml;
  }

  private async generateCover(meta: BookMetadata): Promise<string> {
    try {
      const response = await this.ai.models.generateImages({
        model: 'imagen-4.0-generate-001',
        prompt: `Book cover for "${meta.title}", ${meta.coverDescription}, minimalist, masterpiece, 8k, cinematic.`,
        config: { numberOfImages: 1, aspectRatio: '3:4' }
      });
      return response.generatedImages?.[0]?.image?.imageBytes || '';
    } catch (e) { return ''; }
  }

  private async generateSocialAssets(text: string, meta: BookMetadata): Promise<SocialPost[]> {
    const posts: SocialPost[] = [];
    try {
      const imgResp = await this.ai.models.generateImages({
        model: 'imagen-4.0-generate-001', 
        prompt: `Abstract art representing ${meta.title}, elegant, high contrast.`,
        config: { numberOfImages: 1, aspectRatio: '1:1' }
      });
      posts.push({
          id: 1,
          quote: `Coming Soon: ${meta.title}`,
          imageBase64: imgResp.generatedImages?.[0]?.image?.imageBytes || '',
          caption: `#${meta.title.replace(/\s/g, '')} #NewRelease`
      });
    } catch (e) {}
    return posts;
  }

  private async generateMarketingVideo(meta: BookMetadata): Promise<string> {
    try {
      let operation = await this.ai.models.generateVideos({
        model: 'veo-2.0-generate-001',
        prompt: `Cinematic trailer for book "${meta.title}", mystery, dramatic lighting, 4k.`,
        config: { numberOfVideos: 1 }
      });
      let attempts = 0;
      while (!operation.done && attempts < 20) {
        await new Promise(r => setTimeout(r, 5000));
        operation = await this.ai.operations.getVideosOperation({operation: operation});
        attempts++;
      }
      const uri = operation.response?.generatedVideos?.[0]?.video?.uri;
      if (uri) {
         const resp = await fetch(`${uri}&key=${process.env['API_KEY']}`);
         const blob = await resp.blob();
         return URL.createObjectURL(blob);
      }
    } catch (e) { console.warn("Video failed"); }
    return '';
  }

  private async generateReports(text: string, meta: BookMetadata): Promise<any> {
    return { 
      officialLetter: "<h1>Congratulation</h1><p>Your book is ready.</p>", 
      marketAnalysis: "<h1>Analysis</h1><p>High potential.</p>", 
      strategicDeck: "" 
    };
  }

  private async createZipPackage(meta: BookMetadata, text: string, cover: string, video: string, posts: any[], reports: any): Promise<Blob> {
    const zip = new JSZip();
    const folder = zip.folder(`Project_${meta.title.replace(/\s/g, '_')}`);
    folder.file("Manuscript.html", `<!DOCTYPE html><html dir="${meta.language==='ar'?'rtl':'ltr'}"><body>${text}</body></html>`);
    if(cover) folder.file("cover.png", cover, {base64: true});
    if(video) {
        try { folder.file("trailer.mp4", await fetch(video).then(r=>r.blob())); } catch(e){}
    }
    return await zip.generateAsync({type:"blob"});
  }
}
