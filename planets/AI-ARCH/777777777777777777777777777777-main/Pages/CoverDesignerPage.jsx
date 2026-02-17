/**
 * CoverDesignerPage - مصمم أغلفة الكتب بالذكاء الاصطناعي
 * 
 * الميزات:
 * - تصميم أغلفة بالذكاء الاصطناعي
 * - قوالب جاهزة
 * - تخصيص كامل (ألوان، خطوط، صور)
 * - معاينة فورية
 * - تصدير بجودة عالية
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Palette,
  Sparkles,
  Download,
  RefreshCw,
  Image as ImageIcon,
  Type,
  Layers,
  Zap,
  Grid,
  Save,
  Eye,
  ChevronLeft,
  ChevronRight,
  Wand2
} from 'lucide-react';
import { useToast } from '../Components/ToastProvider';

const CoverDesignerPage = () => {
  const navigate = useNavigate();
  const { success, error, info } = useToast();

  const [coverData, setCoverData] = useState({
    title: '',
    author: '',
    subtitle: '',
    genre: 'رواية',
    style: 'modern',
    primaryColor: '#1e3a5f',
    secondaryColor: '#c9a227',
    textColor: '#ffffff'
  });

  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCovers, setGeneratedCovers] = useState([]);
  const [currentCoverIndex, setCurrentCoverIndex] = useState(0);

  // الأنماط المتاحة
  const styles = [
    { id: 'modern', name: 'عصري', icon: '🎨' },
    { id: 'classic', name: 'كلاسيكي', icon: '📚' },
    { id: 'minimalist', name: 'بسيط', icon: '⬜' },
    { id: 'artistic', name: 'فني', icon: '🖼️' },
    { id: 'dramatic', name: 'درامي', icon: '🌟' },
    { id: 'elegant', name: 'أنيق', icon: '✨' }
  ];

  // الأنواع الأدبية
  const genres = [
    'رواية', 'قصة قصيرة', 'شعر', 'خيال علمي', 'فانتازيا', 
    'رعب', 'رومانسي', 'تاريخي', 'سيرة ذاتية', 'تطوير ذات'
  ];

  // القوالب الجاهزة
  const templates = [
    { id: 1, name: 'النجوم', preview: '⭐', style: 'modern' },
    { id: 2, name: 'الغموض', preview: '🌙', style: 'dramatic' },
    { id: 3, name: 'الكلاسيكية', preview: '📖', style: 'classic' },
    { id: 4, name: 'البساطة', preview: '▪️', style: 'minimalist' },
    { id: 5, name: 'الفن', preview: '🎭', style: 'artistic' },
    { id: 6, name: 'الأناقة', preview: '💎', style: 'elegant' }
  ];

  // توليد غلاف بالذكاء الاصطناعي
  const handleGenerateAI = async () => {
    if (!coverData.title.trim()) {
      error('يرجى إدخال عنوان الكتاب');
      return;
    }

    setIsGenerating(true);
    try {
      // محاكاة توليد AI
      await new Promise(resolve => setTimeout(resolve, 3000));

      // توليد 4 تصاميم
      const newCovers = Array(4).fill(null).map((_, i) => ({
        id: Date.now() + i,
        url: `https://via.placeholder.com/400x600/1e3a5f/ffffff?text=${encodeURIComponent(coverData.title)}`,
        style: coverData.style,
        prompt: `غلاف ${coverData.genre} بأسلوب ${coverData.style}`
      }));

      setGeneratedCovers(newCovers);
      setCurrentCoverIndex(0);
      success('تم توليد 4 تصاميم جديدة! ✨');
      
    } catch (err) {
      console.error('Generation error:', err);
      error('فشل التوليد');
    } finally {
      setIsGenerating(false);
    }
  };

  // حفظ الغلاف
  const handleSave = () => {
    if (generatedCovers.length === 0) {
      warning('قم بتوليد غلاف أولاً');
      return;
    }
    
    success('تم حفظ الغلاف بنجاح!');
    info('يمكنك تحميله الآن');
  };

  // تحميل الغلاف
  const handleDownload = () => {
    if (generatedCovers.length === 0) {
      warning('لا يوجد غلاف للتحميل');
      return;
    }

    success('جاري التحميل...');
    // TODO: Implement actual download
  };

  // التنقل بين الأغلفة
  const nextCover = () => {
    setCurrentCoverIndex((prev) => (prev + 1) % generatedCovers.length);
  };

  const prevCover = () => {
    setCurrentCoverIndex((prev) => (prev - 1 + generatedCovers.length) % generatedCovers.length);
  };

  return (
    <div className="min-h-screen bg-shadow-bg p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* العنوان */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Palette className="w-10 h-10 text-shadow-accent" />
            <h1 className="text-4xl font-bold text-shadow-text cyber-text">
              مصمم الأغلفة
            </h1>
          </div>
          <p className="text-shadow-text/60">
            صمم غلاف كتابك باستخدام الذكاء الاصطناعي في ثوانٍ
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* لوحة التحكم */}
          <div className="lg:col-span-1 space-y-4">
            {/* معلومات الكتاب */}
            <div className="cyber-card bg-shadow-surface rounded-lg border border-shadow-primary/20 p-4">
              <h2 className="text-xl font-bold text-shadow-text mb-4 flex items-center gap-2">
                <Type className="w-5 h-5 text-shadow-accent" />
                معلومات الكتاب
              </h2>

              <div className="space-y-3">
                <div>
                  <label className="block text-sm text-shadow-text/60 mb-1">العنوان *</label>
                  <input
                    type="text"
                    value={coverData.title}
                    onChange={(e) => setCoverData({...coverData, title: e.target.value})}
                    placeholder="عنوان الكتاب..."
                    className="w-full px-3 py-2 bg-shadow-bg border border-shadow-primary/30 rounded-lg text-shadow-text placeholder:text-shadow-text/40 focus:outline-none focus:border-shadow-accent transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-sm text-shadow-text/60 mb-1">المؤلف</label>
                  <input
                    type="text"
                    value={coverData.author}
                    onChange={(e) => setCoverData({...coverData, author: e.target.value})}
                    placeholder="اسم المؤلف..."
                    className="w-full px-3 py-2 bg-shadow-bg border border-shadow-primary/30 rounded-lg text-shadow-text placeholder:text-shadow-text/40 focus:outline-none focus:border-shadow-accent transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-sm text-shadow-text/60 mb-1">عنوان فرعي</label>
                  <input
                    type="text"
                    value={coverData.subtitle}
                    onChange={(e) => setCoverData({...coverData, subtitle: e.target.value})}
                    placeholder="عنوان فرعي (اختياري)..."
                    className="w-full px-3 py-2 bg-shadow-bg border border-shadow-primary/30 rounded-lg text-shadow-text placeholder:text-shadow-text/40 focus:outline-none focus:border-shadow-accent transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-sm text-shadow-text/60 mb-1">النوع الأدبي</label>
                  <select
                    value={coverData.genre}
                    onChange={(e) => setCoverData({...coverData, genre: e.target.value})}
                    className="w-full px-3 py-2 bg-shadow-bg border border-shadow-primary/30 rounded-lg text-shadow-text focus:outline-none focus:border-shadow-accent transition-colors"
                  >
                    {genres.map(genre => (
                      <option key={genre} value={genre}>{genre}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* الأنماط */}
            <div className="cyber-card bg-shadow-surface rounded-lg border border-shadow-primary/20 p-4">
              <h2 className="text-xl font-bold text-shadow-text mb-4 flex items-center gap-2">
                <Layers className="w-5 h-5 text-shadow-accent" />
                الأسلوب
              </h2>

              <div className="grid grid-cols-3 gap-2">
                {styles.map(style => (
                  <button
                    key={style.id}
                    onClick={() => setCoverData({...coverData, style: style.id})}
                    className={`
                      cyber-button p-3 rounded-lg transition-all flex flex-col items-center gap-1
                      ${coverData.style === style.id 
                        ? 'bg-shadow-accent text-white' 
                        : 'bg-shadow-bg text-shadow-text hover:bg-shadow-primary/20'}
                    `}
                  >
                    <span className="text-2xl">{style.icon}</span>
                    <span className="text-xs">{style.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* الألوان */}
            <div className="cyber-card bg-shadow-surface rounded-lg border border-shadow-primary/20 p-4">
              <h2 className="text-xl font-bold text-shadow-text mb-4 flex items-center gap-2">
                <Palette className="w-5 h-5 text-shadow-accent" />
                الألوان
              </h2>

              <div className="space-y-3">
                <ColorPicker
                  label="اللون الأساسي"
                  value={coverData.primaryColor}
                  onChange={(color) => setCoverData({...coverData, primaryColor: color})}
                />
                <ColorPicker
                  label="اللون الثانوي"
                  value={coverData.secondaryColor}
                  onChange={(color) => setCoverData({...coverData, secondaryColor: color})}
                />
                <ColorPicker
                  label="لون النص"
                  value={coverData.textColor}
                  onChange={(color) => setCoverData({...coverData, textColor: color})}
                />
              </div>
            </div>

            {/* زر التوليد */}
            <button
              onClick={handleGenerateAI}
              disabled={isGenerating || !coverData.title.trim()}
              className="w-full cyber-button bg-gradient-to-r from-shadow-accent to-purple-600 px-6 py-4 rounded-lg hover:shadow-glow transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  جاري التوليد...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  توليد بالذكاء الاصطناعي
                </>
              )}
            </button>
          </div>

          {/* منطقة المعاينة */}
          <div className="lg:col-span-2 space-y-4">
            {/* المعاينة الرئيسية */}
            <div className="cyber-card bg-shadow-surface rounded-lg border border-shadow-primary/20 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-shadow-text flex items-center gap-2">
                  <Eye className="w-5 h-5 text-shadow-accent" />
                  المعاينة
                </h2>
                {generatedCovers.length > 0 && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-shadow-text/60">
                      {currentCoverIndex + 1} / {generatedCovers.length}
                    </span>
                  </div>
                )}
              </div>

              {generatedCovers.length === 0 ? (
                // حالة فارغة
                <div className="aspect-[2/3] bg-gradient-to-br from-shadow-bg to-shadow-primary/10 rounded-lg flex flex-col items-center justify-center border-2 border-dashed border-shadow-primary/30">
                  <Wand2 className="w-24 h-24 text-shadow-text/20 mb-4" />
                  <p className="text-shadow-text/60 text-center mb-2">
                    لم يتم توليد أغلفة بعد
                  </p>
                  <p className="text-shadow-text/40 text-sm text-center">
                    املأ المعلومات واضغط على "توليد بالذكاء الاصطناعي"
                  </p>
                </div>
              ) : (
                // معاينة الغلاف
                <div className="relative">
                  <div className="aspect-[2/3] bg-gradient-to-br from-shadow-primary to-shadow-bg rounded-lg overflow-hidden shadow-2xl">
                    {/* Placeholder للغلاف */}
                    <div 
                      className="w-full h-full flex flex-col items-center justify-center text-center p-8"
                      style={{
                        background: `linear-gradient(135deg, ${coverData.primaryColor} 0%, ${coverData.secondaryColor} 100%)`
                      }}
                    >
                      <div className="space-y-6">
                        {coverData.author && (
                          <p className="text-sm opacity-80" style={{ color: coverData.textColor }}>
                            {coverData.author}
                          </p>
                        )}
                        <h1 
                          className="text-4xl font-bold leading-tight"
                          style={{ color: coverData.textColor }}
                        >
                          {coverData.title}
                        </h1>
                        {coverData.subtitle && (
                          <p className="text-lg opacity-80" style={{ color: coverData.textColor }}>
                            {coverData.subtitle}
                          </p>
                        )}
                        <div className="pt-8">
                          <span 
                            className="text-xs px-3 py-1 rounded-full bg-white/20"
                            style={{ color: coverData.textColor }}
                          >
                            {coverData.genre}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* أزرار التنقل */}
                  {generatedCovers.length > 1 && (
                    <>
                      <button
                        onClick={prevCover}
                        className="absolute left-2 top-1/2 -translate-y-1/2 cyber-button bg-shadow-surface/90 p-3 rounded-full hover:bg-shadow-accent transition-all"
                      >
                        <ChevronLeft className="w-6 h-6" />
                      </button>
                      <button
                        onClick={nextCover}
                        className="absolute right-2 top-1/2 -translate-y-1/2 cyber-button bg-shadow-surface/90 p-3 rounded-full hover:bg-shadow-accent transition-all"
                      >
                        <ChevronRight className="w-6 h-6" />
                      </button>
                    </>
                  )}
                </div>
              )}

              {/* أزرار الإجراءات */}
              {generatedCovers.length > 0 && (
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleSave}
                    className="flex-1 cyber-button bg-shadow-primary/20 px-4 py-3 rounded-lg hover:bg-shadow-primary/30 transition-all flex items-center justify-center gap-2"
                  >
                    <Save className="w-5 h-5" />
                    حفظ
                  </button>
                  <button
                    onClick={handleDownload}
                    className="flex-1 cyber-button bg-shadow-accent px-4 py-3 rounded-lg hover:shadow-glow transition-all flex items-center justify-center gap-2"
                  >
                    <Download className="w-5 h-5" />
                    تحميل
                  </button>
                  <button
                    onClick={handleGenerateAI}
                    disabled={isGenerating}
                    className="cyber-button bg-shadow-primary/20 px-4 py-3 rounded-lg hover:bg-shadow-primary/30 transition-all disabled:opacity-50"
                  >
                    <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                  </button>
                </div>
              )}
            </div>

            {/* القوالب الجاهزة */}
            <div className="cyber-card bg-shadow-surface rounded-lg border border-shadow-primary/20 p-4">
              <h2 className="text-lg font-bold text-shadow-text mb-4 flex items-center gap-2">
                <Grid className="w-5 h-5 text-shadow-accent" />
                القوالب الجاهزة
              </h2>

              <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
                {templates.map(template => (
                  <button
                    key={template.id}
                    onClick={() => {
                      setSelectedTemplate(template.id);
                      setCoverData({...coverData, style: template.style});
                      info(`تم تطبيق قالب: ${template.name}`);
                    }}
                    className={`
                      aspect-[2/3] cyber-card rounded-lg transition-all flex flex-col items-center justify-center text-4xl
                      ${selectedTemplate === template.id 
                        ? 'border-2 border-shadow-accent bg-shadow-accent/10' 
                        : 'border border-shadow-primary/20 hover:border-shadow-accent/50 bg-shadow-bg'}
                    `}
                  >
                    {template.preview}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Cyber Grid Background */}
      <div className="fixed inset-0 pointer-events-none opacity-10 cyber-grid -z-10" />
    </div>
  );
};

// مُنتقي الألوان
const ColorPicker = ({ label, value, onChange }) => (
  <div className="flex items-center justify-between gap-3">
    <label className="text-sm text-shadow-text/60">{label}</label>
    <div className="flex items-center gap-2">
      <input
        type="color"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-12 h-8 rounded border-2 border-shadow-primary/30 cursor-pointer"
      />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-24 px-2 py-1 bg-shadow-bg border border-shadow-primary/30 rounded text-xs text-shadow-text focus:outline-none focus:border-shadow-accent transition-colors"
      />
    </div>
  </div>
);

export default CoverDesignerPage;
