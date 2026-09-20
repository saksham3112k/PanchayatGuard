with open('src/pages/Settings.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The block to split is:
old_block = """         {(activeTab === 'Notifications' || activeTab === 'Dashboard Preferences' ) && (
            <div className="space-y-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Notification Preferences</h3>
                  <div className="space-y-4">
                     {[
                        { k: 'highRisk', title: 'High-risk alerts', desc: 'Get notified about critical risk alerts', c: 'text-red-500' },
                        { k: 'newGrievances', title: 'New grievances', desc: 'Get notified about new grievances', c: 'text-blue-500' },
                        { k: 'reportGen', title: 'Report generation', desc: 'Get notified when reports are ready', c: 'text-green-500' },
                        { k: 'emailNotifs', title: 'Email notifications', desc: 'Receive important notifications via email', c: 'text-gray-600' }
                     ].map(n => (
                        <div key={n.k} className="flex justify-between items-center">
                           <div>
                              <h4 className="text-sm font-bold text-gray-800">{n.title}</h4>
                              <p className="text-xs text-gray-500">{n.desc}</p>
                           </div>
                           <button onClick={()=>handleNotifToggle(n.k as keyof typeof notifs)} className={`w-10 h-5 rounded-full relative transition-colors ${notifs[n.k as keyof typeof notifs] ? 'bg-pg-blue':'bg-gray-300'}`}>
                              <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-all ${notifs[n.k as keyof typeof notifs] ? 'left-5':'left-1'}`}/>
                           </button>
                        </div>
                     ))}
                  </div>
               </div>

               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Dashboard Preferences</h3>
                  <div className="space-y-4">
                     <div className="grid grid-cols-2 gap-4">
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Default District</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.district} onChange={e=>handlePrefChange('district', e.target.value)}>
                              <option>All Districts</option><option>Kanpur</option><option>Lucknow</option>
                           </select>
                        </div>
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Theme</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.theme} onChange={e=>handlePrefChange('theme', e.target.value)}>
                              <option>Light</option><option>Dark</option><option>System</option>
                           </select>
                        </div>
                     </div>
                     <div className="flex items-center gap-2">
                        <input type="checkbox" id="ai-toggle" checked={prefs.showAi} onChange={e=>handlePrefChange('showAi', e.target.checked)} className="rounded text-pg-blue focus:ring-pg-blue" />
                        <label htmlFor="ai-toggle" className="text-sm text-gray-700 font-medium">Show AI insights on dashboard</label>
                     </div>
                  </div>
               </div>
            </div>
         )}"""

new_block = """         {(activeTab === 'Notifications') && (
            <div className="space-y-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Notification Preferences</h3>
                  <div className="space-y-4">
                     {[
                        { k: 'highRisk', title: 'High-risk alerts', desc: 'Get notified about critical risk alerts', c: 'text-red-500' },
                        { k: 'newGrievances', title: 'New grievances', desc: 'Get notified about new grievances', c: 'text-blue-500' },
                        { k: 'reportGen', title: 'Report generation', desc: 'Get notified when reports are ready', c: 'text-green-500' },
                        { k: 'emailNotifs', title: 'Email notifications', desc: 'Receive important notifications via email', c: 'text-gray-600' }
                     ].map(n => (
                        <div key={n.k} className="flex justify-between items-center">
                           <div>
                              <h4 className="text-sm font-bold text-gray-800">{n.title}</h4>
                              <p className="text-xs text-gray-500">{n.desc}</p>
                           </div>
                           <button onClick={()=>handleNotifToggle(n.k as keyof typeof notifs)} className={`w-10 h-5 rounded-full relative transition-colors ${notifs[n.k as keyof typeof notifs] ? 'bg-pg-blue':'bg-gray-300'}`}>
                              <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-all ${notifs[n.k as keyof typeof notifs] ? 'left-5':'left-1'}`}/>
                           </button>
                        </div>
                     ))}
                  </div>
               </div>
            </div>
         )}

         {(activeTab === 'Dashboard Preferences') && (
            <div className="space-y-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Dashboard Preferences</h3>
                  <div className="space-y-4">
                     <div className="grid grid-cols-2 gap-4">
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Default District</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.district} onChange={e=>handlePrefChange('district', e.target.value)}>
                              <option>All Districts</option><option>Kanpur</option><option>Lucknow</option><option>Varanasi</option>
                           </select>
                        </div>
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Theme</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.theme} onChange={e=>{
                               handlePrefChange('theme', e.target.value);
                               if(e.target.value === 'Dark') {
                                   document.body.classList.add('dark-theme');
                               } else {
                                   document.body.classList.remove('dark-theme');
                               }
                               // Fire an event so AppLayout can listen
                               window.dispatchEvent(new Event('theme_changed'));
                           }}>
                              <option>Light</option><option>Dark</option><option>System</option>
                           </select>
                        </div>
                     </div>
                     <div className="flex items-center gap-2">
                        <input type="checkbox" id="ai-toggle" checked={prefs.showAi} onChange={e=>handlePrefChange('showAi', e.target.checked)} className="rounded text-pg-blue focus:ring-pg-blue" />
                        <label htmlFor="ai-toggle" className="text-sm text-gray-700 font-medium">Show AI insights on dashboard</label>
                     </div>
                  </div>
               </div>
            </div>
         )}"""

# We need to replace the old_block with new_block.
# But just in case indentation is tricky, I'll use regex.
import re
content = re.sub(r"\{\(activeTab === 'Notifications' \|\| activeTab === 'Dashboard Preferences' \).*?Show AI insights on dashboard</label>\s*</div>\s*</div>\s*</div>\s*</div>\s*\)}", new_block, content, flags=re.DOTALL)

# Add District event dispatch
content = content.replace("handlePrefChange = (k: keyof typeof prefs, v: any) => {", "handlePrefChange = (k: keyof typeof prefs, v: any) => {\n        if (k === 'district') window.dispatchEvent(new Event('theme_changed'));")

with open('src/pages/Settings.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
