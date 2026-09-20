import React, { useState, useEffect } from 'react';
import { Outlet, Navigate, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { 
  LayoutDashboard, ShoppingCart, Users, AlertTriangle, Receipt, Map, 
  BarChart, Brain, MessageSquare, ShieldAlert, Settings, LogOut, ShieldCheck,
  Search, MapPin, Bell, ChevronDown, Menu, X
} from 'lucide-react';
import api from '../services/api';
import TransactionDetails from '../components/TransactionDetails';

const MENU_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Procurement', path: '/procurement', icon: ShoppingCart },
  { name: 'Vendors', path: '/vendors', icon: Users },
  { name: 'Risk Analysis', path: '/risk-analysis', icon: AlertTriangle },
  { name: 'Transactions', path: '/transactions', icon: Receipt },
  { name: 'Geographic View', path: '/geo', icon: Map },
  { name: 'Reports', path: '/reports', icon: BarChart },
  { name: 'AI Insights', path: '/ai', icon: Brain },
  { name: 'Grievances', path: '/grievances', icon: MessageSquare },
  { name: 'Audit Logs', path: '/audit', icon: ShieldAlert },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

    const handleSearchClick = (res: any) => {
        setSearchQuery('');
        setSearchResults([]);
        if (res.type === 'Vendor') {
            navigate(`/vendors/${res.id}`);
        } else if (res.type === 'Transaction') {
            setViewingTxId(res.id);
        } else if (res.type === 'Panchayat') {
            navigate('/geo');
        }
    };

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
    const [viewingTxId, setViewingTxId] = useState<number | null>(null);
    const [currentDistrict, setCurrentDistrict] = useState('Uttar Pradesh');

  const [notifs, setNotifs] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifs, setShowNotifs] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if(user) {
       api.get('/notifications').then(res => {
         setNotifs(res.data.notifications);
         setUnreadCount(res.data.unread_count);
       });
    }
  }, [user]);

  const markAsRead = async (id: number) => {
     await api.put(`/notifications/${id}/read`);
     setNotifs(notifs.map(n => n.id === id ? {...n, is_read: true} : n));
     setUnreadCount(Math.max(0, unreadCount - 1));
  };
  
  const markAllRead = async () => {
     await api.put(`/notifications/read-all`);
     setNotifs(notifs.map(n => ({...n, is_read: true})));
     setUnreadCount(0);
  };


  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (searchQuery.length >= 2) {
        try {
          const res = await api.get(`/dashboard/search?q=${searchQuery}`);
          setSearchResults(res.data);
        } catch (e) {
          console.error(e);
        }
      } else {
        setSearchResults([]);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex h-screen bg-pg-light">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-pg-navy text-gray-300 flex flex-col h-full transform transition-transform duration-300 md:relative md:translate-x-0 ${mobileMenuOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="p-5 flex items-center gap-3">
          <button className="md:hidden absolute top-4 right-4 text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
            <X className="w-6 h-6" />
          </button>
          <div className="bg-white p-1 rounded">
            <ShieldCheck className="w-7 h-7 text-pg-green" />
          </div>
          <div>
            <span className="text-white font-bold text-lg block leading-tight">PanchayatGuard</span>
            <span className="text-[10px] text-gray-400 block leading-tight">Transparent Panchayat. Stronger Bharat.</span>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto py-4">
          <nav className="space-y-1 px-3">
            {MENU_ITEMS.map((item) => {
              const active = location.pathname === item.path;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${active ? 'bg-pg-blue text-white' : 'hover:bg-gray-800 hover:text-white'}`}
                >
                  <item.icon className={`w-5 h-5 ${active ? 'text-white' : 'text-gray-400'}`} />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="p-5">
           <div className="text-center">
              <div className="flex justify-center mb-2 opacity-50">
                {/* SVG for decorative graphic can go here */}
              </div>
              <p className="text-[10px] text-gray-500">Digital Governance<br/>for Stronger Communities</p>
           </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-white flex items-center justify-between px-6 flex-shrink-0 z-10 shadow-sm relative">
          <div className="flex items-center w-full md:w-1/2 max-w-lg relative gap-3">
             <button className="md:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded" onClick={() => setMobileMenuOpen(true)}>
             <Menu className="w-6 h-6" />
          </button>
             <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
               <Search className="h-4 w-4 text-gray-400" />
             </div>
             <input 
               type="text"
               value={searchQuery}
               onChange={(e) => setSearchQuery(e.target.value)}
               placeholder="Search transactions, vendors, panchayats..."
               className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-pg-blue focus:bg-white"
             />
             
             {/* Search Dropdown */}
             {searchResults.length > 0 && (
               <div className="absolute top-full mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50 py-2 max-h-64 overflow-y-auto">
                 {searchResults.map((res, i) => (
                   <div key={i} onClick={() => handleSearchClick(res)} className="px-4 py-2 hover:bg-gray-50 cursor-pointer">
                     <span className="text-xs font-semibold text-pg-blue bg-blue-50 px-2 py-0.5 rounded mr-2">{res.type}</span>
                     <span className="text-sm text-gray-800">{res.title}</span>
                   </div>
                 ))}
               </div>
             )}
          </div>
          
          <div className="flex items-center gap-6">
             <div className="flex items-center gap-1 text-sm text-gray-600 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200 cursor-pointer">
               <MapPin className="w-4 h-4" />
               <span>{currentDistrict}</span>
               <ChevronDown className="w-4 h-4 ml-1" />
             </div>
             
             <div className="relative cursor-pointer" onClick={() => setShowNotifs(!showNotifs)}>
               <Bell className="w-5 h-5 text-gray-600" />
               {unreadCount > 0 && <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[10px] text-white font-bold">{unreadCount}</span>}
               
               {showNotifs && (
                 <div className="absolute top-full right-0 mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-xl z-50 overflow-hidden cursor-default" onClick={e=>e.stopPropagation()}>
                    <div className="p-3 border-b flex justify-between items-center bg-gray-50">
                       <h3 className="font-bold text-gray-800">Notifications</h3>
                       <button onClick={markAllRead} className="text-xs text-pg-blue hover:underline">Mark all as read</button>
                    </div>
                    <div className="max-h-80 overflow-y-auto divide-y divide-gray-100">
                       {notifs.map(n => (
                          <div key={n.id} className={`p-4 flex gap-3 ${!n.is_read ? 'bg-blue-50/30' : ''}`}>
                             <div className={`p-2 rounded-full h-fit ${n.type==='alert' ? 'bg-red-100 text-red-500' : 'bg-blue-100 text-pg-blue'}`}>
                                <AlertTriangle className="w-4 h-4"/>
                             </div>
                             <div className="flex-1">
                                <h4 className="text-sm font-semibold text-gray-900">{n.title}</h4>
                                <p className="text-xs text-gray-600 mt-1">{n.message}</p>
                                <div className="text-[10px] text-gray-400 mt-2 flex justify-between">
                                   <span>{new Date(n.created_at).toLocaleString()}</span>
                                   {!n.is_read && <button onClick={()=>markAsRead(n.id)} className="text-pg-blue hover:underline font-semibold">Mark read</button>}
                                </div>
                             </div>
                          </div>
                       ))}
                       {notifs.length === 0 && <div className="p-6 text-center text-sm text-gray-500">No notifications</div>}
                    </div>
                 </div>
               )}
             </div>
             
             
    <div className="relative group">
       <div className="flex items-center gap-3 cursor-pointer hover:bg-gray-50 p-2 rounded-lg transition-colors">
    
               <div className="w-8 h-8 rounded-full bg-pg-navy flex items-center justify-center text-white font-bold text-sm">
                 {user.name.split(' ').map(n => n[0]).join('')}
               </div>
               <div className="hidden md:block">
                 <p className="text-sm font-semibold text-gray-800 leading-tight">{user.name}</p>
                 <p className="text-xs text-gray-500 leading-tight">{user.role}</p>
               </div>
               <ChevronDown className="w-4 h-4 text-gray-500 hidden md:block" />
             </div>
             
             <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <div className="p-2 border-b border-gray-100">
                  <p className="text-sm font-bold text-gray-900">{user.name}</p>
                  <p className="text-xs text-gray-500 truncate">{user.email}</p>
                </div>
                <div className="p-1">
                  <button onClick={() => navigate('/settings')} className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md flex items-center gap-2">
                    <Settings className="w-4 h-4" /> Settings
                  </button>
                  <button onClick={logout} className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md flex items-center gap-2">
                    <LogOut className="w-4 h-4" /> Logout
                  </button>
                </div>
              </div>
          </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto bg-pg-light p-6">
          <Outlet />
        </main>
        {viewingTxId && <TransactionDetails isOpen={true} txId={viewingTxId} onClose={() => setViewingTxId(null)} />}
      </div>
    </div>
  );
}
