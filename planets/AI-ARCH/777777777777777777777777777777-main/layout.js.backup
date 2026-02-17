import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { createPageUrl } from "./utils";
import { base44 } from "@/api/base44Client";
import {
  BookOpen,
  Upload,
  FileText,
  Palette,
  Shield,
  Settings,
  Menu,
  X,
  ChevronLeft,
  LogOut,
  User,
  Home,
  Layers,
  BookCopy,
  Sparkles
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function Layout({ children, currentPageName }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    base44.auth.me().then(setUser).catch(() => {});
  }, []);

  const navigation = [
    { name: "الرئيسية", page: "Dashboard", icon: Home },
    { name: "المخطوطات", page: "Manuscripts", icon: BookOpen },
    { name: "رفع مخطوطة", page: "Upload", icon: Upload },
    { name: "المحرر النخبة", page: "EliteEditor", icon: Sparkles },
    { name: "دمج الكتب", page: "BookMerger", icon: BookCopy },
    { name: "تقسيم السلاسل", page: "SeriesSplitter", icon: Layers },
    { name: "تصميم الأغلفة", page: "CoverDesigner", icon: Palette },
    { name: "محرك الامتثال", page: "ComplianceEngine", icon: Shield },
    { name: "الإعدادات", page: "Settings", icon: Settings },
  ];

  return (
    <div dir="rtl" className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <style>{`
        :root {
          --color-primary: #1e3a5f;
          --color-secondary: #2563eb;
          --color-accent: #c9a227;
          --color-surface: #ffffff;
          --color-muted: #64748b;
        }
        
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
        
        .nav-item {
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .nav-item:hover {
          transform: translateX(-4px);
        }
        
        .nav-item.active {
          background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
          color: white;
          box-shadow: 0 4px 15px rgba(30, 58, 95, 0.3);
        }
        
        .sidebar-gradient {
          background: linear-gradient(180deg, #fafbfc 0%, #f1f5f9 100%);
        }
        
        .logo-text {
          background: linear-gradient(135deg, #1e3a5f 0%, #c9a227 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
      `}</style>

      {/* Sidebar */}
      <aside
        className={`fixed right-0 top-0 h-full sidebar-gradient border-l border-slate-200/60 z-50 transition-all duration-500 ease-out ${
          sidebarOpen ? "w-72" : "w-20"
        }`}
      >
        {/* Logo */}
        <div className="h-20 flex items-center justify-between px-6 border-b border-slate-200/60">
          {sidebarOpen && (
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#1e3a5f] to-[#2563eb] flex items-center justify-center shadow-lg">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold logo-text">سيادي</h1>
                <p className="text-xs text-slate-500">AI Publishing Engine</p>
              </div>
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="hover:bg-slate-200/50"
          >
            {sidebarOpen ? <ChevronLeft className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </Button>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = currentPageName === item.page;
            return (
              <Link
                key={item.page}
                to={createPageUrl(item.page)}
                className={`nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium ${
                  isActive
                    ? "active"
                    : "text-slate-600 hover:bg-slate-200/50"
                }`}
              >
                <Icon className={`w-5 h-5 ${!sidebarOpen ? "mx-auto" : ""}`} />
                {sidebarOpen && <span>{item.name}</span>}
              </Link>
            );
          })}
        </nav>

        {/* User Section */}
        {user && sidebarOpen && (
          <div className="absolute bottom-0 right-0 left-0 p-4 border-t border-slate-200/60">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-200/50 transition-colors">
                  <Avatar className="w-10 h-10 bg-gradient-to-br from-[#1e3a5f] to-[#2563eb]">
                    <AvatarFallback className="text-white font-medium">
                      {user.full_name?.charAt(0) || user.email?.charAt(0)}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 text-right">
                    <p className="text-sm font-medium text-slate-800">{user.full_name || "مستخدم"}</p>
                    <p className="text-xs text-slate-500">{user.email}</p>
                  </div>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem onClick={() => base44.auth.logout()}>
                  <LogOut className="w-4 h-4 ml-2" />
                  تسجيل الخروج
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main
        className={`transition-all duration-500 ${
          sidebarOpen ? "mr-72" : "mr-20"
        }`}
      >
        <div className="min-h-screen">
          {children}
        </div>
      </main>
    </div>
  );
}