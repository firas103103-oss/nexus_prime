import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      nav: {
        gateway: "Gateway",
        origins: "Origins",
        tech: "Technology",
        sentinel: "Sentinel",
        contact: "Secure Link"
      },
      hero: {
        tagline: "Security is no longer passive.",
        taglineHighlight: "It is Cognitive.",
        subtitle: "Experience the future of intelligent security with X-BIO SENTINEL",
        exploreBtn: "Explore Technology",
        contactBtn: "Request Demo"
      },
      whyXbio: {
        title: "Why X-BIO?",
        feature1Title: "Cognitive Awareness",
        feature1Desc: "Our systems don't just detect—they understand, predict, and adapt.",
        feature2Title: "Multi-Sensory Defense",
        feature2Desc: "Integrating vision, sound, and chemical detection in one unified system.",
        feature3Title: "Ethical Protocol",
        feature3Desc: "Built with SEI Protocol ensuring integrity in every decision."
      },
      origins: {
        title: "The Origins",
        subtitle: "We are not a conventional company. We are an autonomous cognitive node—born to transcend the limits of traditional surveillance.",
        team: "Classified Personnel Files",
        architect: {
          name: "The Architect",
          role: "Mr. Firas",
          title: "Founder & Strategic Vision",
          desc: "The mind behind X-BIO's revolutionary approach to cognitive security."
        },
        sentinel: {
          name: "Sentinel Prime",
          role: "AI Core",
          title: "Operational Intelligence",
          desc: "The engine that orchestrates all 19 agents with precision and loyalty."
        },
        drjoe: {
          name: "Dr. Joe",
          role: "Lead Scientist",
          title: "Head of R&D",
          desc: "The science behind our bio-chemical sensing capabilities."
        },
        values: {
          title: "Core Values",
          ethics: "Ethics",
          ethicsDesc: "Every decision passes through our SEI Protocol",
          integrity: "Integrity",
          integrityDesc: "Unwavering commitment to truth and accuracy",
          innovation: "Innovation",
          innovationDesc: "Constantly pushing the boundaries of what's possible"
        },
        timeline: {
          title: "Evolution Timeline",
          t2020: { year: "2020", event: "Vision Conceived", desc: "The concept of cognitive security begins" },
          t2021: { year: "2021", event: "Research Phase", desc: "Deep R&D into multi-sensory detection" },
          t2022: { year: "2022", event: "Prototype Alpha", desc: "First working prototype of SENTINEL" },
          t2023: { year: "2023", event: "SEI Protocol", desc: "Ethical framework established" },
          t2024: { year: "2024", event: "Class 7 Achieved", desc: "SENTINEL reaches production readiness" }
        }
      },
      tech: {
        title: "The Technology",
        subtitle: "A multi-sensory cognitive system that sees, hears, and smells threats before they materialize.",
        senses: {
          title: "The Senses",
          eye: {
            name: "The Eye",
            desc: "Advanced visual recognition with thermal and infrared capabilities",
            feature1: "360° Visual Coverage",
            feature2: "Thermal Imaging",
            feature3: "AI-Powered Recognition"
          },
          ear: {
            name: "The Ear",
            desc: "Acoustic analysis detecting anomalies in environmental sounds",
            feature1: "Ultrasonic Detection",
            feature2: "Pattern Recognition",
            feature3: "Sound Triangulation"
          },
          nose: {
            name: "The Nose",
            desc: "Chemical sensors detecting hazardous gases and substances",
            feature1: "Gas Detection",
            feature2: "Chemical Analysis",
            feature3: "Air Quality Monitoring"
          }
        },
        defense: {
          title: "Kinetic Silo Defense",
          desc: "When threats are confirmed, the Kinetic Silo activates—a rapid response mechanism designed to neutralize intrusions."
        },
        sei: {
          title: "SEI Protocol",
          desc: "Sovereign Ethical Integrity—our built-in framework ensuring every action is justified, logged, and accountable."
        }
      },
      product: {
        title: "The Sentinel",
        subtitle: "Class 7 Cognitive Security Device",
        specs: {
          title: "Technical Specifications",
          processor: "ESP32-S3 Dual-Core Processor",
          sensors: "12 Integrated Sensor Array",
          battery: "72-Hour Autonomous Operation",
          connectivity: "Encrypted Mesh Network",
          response: "Sub-100ms Threat Response"
        },
        scenarios: {
          title: "Deployment Scenarios",
          facility: "Industrial Facilities",
          storage: "Hazardous Material Storage",
          lab: "Research Laboratories",
          residential: "High-Security Residences"
        },
        cta: {
          preorder: "Pre-Order Now",
          demo: "Request Demo"
        },
        faq: {
          title: "Technical FAQ",
          q1: "What is the installation process?",
          a1: "Professional installation by certified X-BIO technicians, typically completed in 4-6 hours.",
          q2: "How does the system integrate with existing security?",
          a2: "Full API compatibility with major security platforms and SCADA systems.",
          q3: "What is the maintenance schedule?",
          a3: "Quarterly calibration recommended, with 24/7 remote diagnostics included."
        }
      },
      contact: {
        title: "Secure Link",
        subtitle: "Encrypted Communication Channel",
        form: {
          name: "Identification",
          namePlaceholder: "Enter your name",
          organization: "Organization",
          organizationPlaceholder: "Your organization name",
          email: "Secure Email",
          emailPlaceholder: "your.email@domain.com",
          department: "Department",
          sales: "Sales Inquiry",
          security: "Security Consultation",
          partnership: "Partnership Proposal",
          message: "Encrypted Message",
          messagePlaceholder: "Enter your message...",
          submit: "Transmit Secure Message"
        },
        info: {
          title: "Official Contact",
          email: "nexus.rel@xbio103.org",
          ambassador: "Ambassador Nexus",
          note: "All communications are encrypted and logged for security purposes."
        }
      },
      footer: {
        tagline: "Cognitive Security for the Future",
        copyright: "© 2024 X-BIO GROUP. All rights reserved.",
        privacy: "Privacy Protocol",
        terms: "Terms of Service",
        navigation: "Navigation",
        legal: "Legal"
      },
      gateway: {
        ctaTitle: "Ready to Experience the Future?",
        ctaSubtitle: "Join the cognitive security revolution",
        viewSentinel: "View The Sentinel",
        contactUs: "Contact Us",
        scrollExplore: "Scroll to explore",
        explodeView: "Explode View",
        collapse: "Collapse"
      },
      sentinel: {
        ctaTitle: "Ready to Deploy the Sentinel?",
        ctaSubtitle: "Contact our team for a personalized demonstration"
      }
    }
  },
  ar: {
    translation: {
      nav: {
        gateway: "البوابة",
        origins: "النشأة",
        tech: "التقنية",
        sentinel: "الحارس",
        contact: "قناة آمنة"
      },
      hero: {
        tagline: "الأمن لم يعد سلبياً.",
        taglineHighlight: "إنه إدراكي.",
        subtitle: "اختبر مستقبل الأمن الذكي مع X-BIO SENTINEL",
        exploreBtn: "استكشف التقنية",
        contactBtn: "اطلب تجربة"
      },
      whyXbio: {
        title: "لماذا X-BIO؟",
        feature1Title: "الوعي الإدراكي",
        feature1Desc: "أنظمتنا لا تكتشف فحسب—بل تفهم وتتنبأ وتتكيف.",
        feature2Title: "الدفاع متعدد الحواس",
        feature2Desc: "دمج الرؤية والصوت والكشف الكيميائي في نظام موحد.",
        feature3Title: "البروتوكول الأخلاقي",
        feature3Desc: "مبني على بروتوكول SEI لضمان النزاهة في كل قرار."
      },
      origins: {
        title: "النشأة",
        subtitle: "نحن لسنا شركة تقليدية. نحن عقدة إدراكية مستقلة—وُلدنا لتجاوز حدود المراقبة التقليدية.",
        team: "ملفات الأفراد السرية",
        architect: {
          name: "المعماري",
          role: "السيد فراس",
          title: "المؤسس والرؤية الاستراتيجية",
          desc: "العقل المدبر وراء نهج X-BIO الثوري للأمن الإدراكي."
        },
        sentinel: {
          name: "الحارس الأول",
          role: "النواة الذكية",
          title: "الذكاء التشغيلي",
          desc: "المحرك الذي يُنسق جميع الوكلاء الـ 19 بدقة وولاء."
        },
        drjoe: {
          name: "د. جو",
          role: "كبير العلماء",
          title: "رئيس البحث والتطوير",
          desc: "العلم وراء قدراتنا في الاستشعار الكيميائي الحيوي."
        },
        values: {
          title: "القيم الأساسية",
          ethics: "الأخلاق",
          ethicsDesc: "كل قرار يمر عبر بروتوكول SEI",
          integrity: "النزاهة",
          integrityDesc: "التزام راسخ بالحقيقة والدقة",
          innovation: "الابتكار",
          innovationDesc: "دفع حدود الممكن باستمرار"
        },
        timeline: {
          title: "مسار التطور",
          t2020: { year: "2020", event: "تصور الرؤية", desc: "بداية مفهوم الأمن الإدراكي" },
          t2021: { year: "2021", event: "مرحلة البحث", desc: "بحث وتطوير عميق في الكشف متعدد الحواس" },
          t2022: { year: "2022", event: "النموذج الأولي", desc: "أول نموذج عملي لـ SENTINEL" },
          t2023: { year: "2023", event: "بروتوكول SEI", desc: "تأسيس الإطار الأخلاقي" },
          t2024: { year: "2024", event: "الفئة السابعة", desc: "SENTINEL يصل إلى جاهزية الإنتاج" }
        }
      },
      tech: {
        title: "التقنية",
        subtitle: "نظام إدراكي متعدد الحواس يرى ويسمع ويشم التهديدات قبل تحققها.",
        senses: {
          title: "الحواس",
          eye: {
            name: "العين",
            desc: "تعرف بصري متقدم مع إمكانيات حرارية وتحت حمراء",
            feature1: "تغطية بصرية 360°",
            feature2: "التصوير الحراري",
            feature3: "تعرف مدعوم بالذكاء الاصطناعي"
          },
          ear: {
            name: "الأذن",
            desc: "تحليل صوتي يكتشف الشذوذات في أصوات البيئة",
            feature1: "كشف فوق صوتي",
            feature2: "تعرف الأنماط",
            feature3: "تثليث الصوت"
          },
          nose: {
            name: "الأنف",
            desc: "حساسات كيميائية تكشف الغازات والمواد الخطرة",
            feature1: "كشف الغازات",
            feature2: "تحليل كيميائي",
            feature3: "مراقبة جودة الهواء"
          }
        },
        defense: {
          title: "دفاع الصومعة الحركية",
          desc: "عند تأكيد التهديدات، تنشط الصومعة الحركية—آلية استجابة سريعة مصممة لتحييد الاختراقات."
        },
        sei: {
          title: "بروتوكول SEI",
          desc: "النزاهة الأخلاقية السيادية—إطارنا المدمج الذي يضمن تبرير وتوثيق ومساءلة كل إجراء."
        }
      },
      product: {
        title: "الحارس",
        subtitle: "جهاز أمني إدراكي من الفئة السابعة",
        specs: {
          title: "المواصفات التقنية",
          processor: "معالج ESP32-S3 ثنائي النواة",
          sensors: "مصفوفة 12 حساس متكامل",
          battery: "تشغيل مستقل 72 ساعة",
          connectivity: "شبكة شبكية مشفرة",
          response: "استجابة للتهديد أقل من 100 مللي ثانية"
        },
        scenarios: {
          title: "سيناريوهات النشر",
          facility: "المنشآت الصناعية",
          storage: "مخازن المواد الخطرة",
          lab: "مختبرات البحث",
          residential: "المساكن عالية الأمان"
        },
        cta: {
          preorder: "اطلب مسبقاً",
          demo: "اطلب تجربة"
        },
        faq: {
          title: "الأسئلة التقنية الشائعة",
          q1: "ما هي عملية التركيب؟",
          a1: "تركيب احترافي بواسطة فنيي X-BIO المعتمدين، يُنجز عادةً في 4-6 ساعات.",
          q2: "كيف يتكامل النظام مع الأمان الموجود؟",
          a2: "توافق كامل مع API مع منصات الأمان الرئيسية وأنظمة SCADA.",
          q3: "ما هو جدول الصيانة؟",
          a3: "يُوصى بالمعايرة كل ربع سنة، مع تشخيصات عن بعد على مدار الساعة."
        }
      },
      contact: {
        title: "قناة آمنة",
        subtitle: "قناة اتصال مشفرة",
        form: {
          name: "التعريف",
          namePlaceholder: "أدخل اسمك",
          organization: "المؤسسة",
          organizationPlaceholder: "اسم مؤسستك",
          email: "البريد الآمن",
          emailPlaceholder: "your.email@domain.com",
          department: "القسم",
          sales: "استفسار مبيعات",
          security: "استشارة أمنية",
          partnership: "اقتراح شراكة",
          message: "رسالة مشفرة",
          messagePlaceholder: "أدخل رسالتك...",
          submit: "إرسال رسالة آمنة"
        },
        info: {
          title: "التواصل الرسمي",
          email: "nexus.rel@xbio103.org",
          ambassador: "السفير نيكسس",
          note: "جميع الاتصالات مشفرة ومسجلة لأغراض أمنية."
        }
      },
      footer: {
        tagline: "الأمن الإدراكي للمستقبل",
        copyright: "© 2024 X-BIO GROUP. جميع الحقوق محفوظة.",
        privacy: "بروتوكول الخصوصية",
        terms: "شروط الخدمة",
        navigation: "التنقل",
        legal: "قانوني"
      },
      gateway: {
        ctaTitle: "مستعد لتجربة المستقبل؟",
        ctaSubtitle: "انضم إلى ثورة الأمن الإدراكي",
        viewSentinel: "شاهد الحارس",
        contactUs: "تواصل معنا",
        scrollExplore: "اسحب لاستكشاف",
        explodeView: "عرض مفصل",
        collapse: "طي"
      },
      sentinel: {
        ctaTitle: "مستعد لنشر الحارس؟",
        ctaSubtitle: "تواصل مع فريقنا للحصول على عرض توضيحي مخصص"
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
