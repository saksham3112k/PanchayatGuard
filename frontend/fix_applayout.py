with open('src/layouts/AppLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
'''               <div className="hidden md:block">
                 <p className="text-sm font-semibold text-gray-800 leading-tight">{user.name}</p>
                 <p className="text-xs text-gray-500 leading-tight">{user.role}</p>
               </div>
             </div>
          </div>
        </header>''',
'''               <div className="hidden md:block">
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
        </header>'''
)

with open('src/layouts/AppLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
