with open('src/pages/Login.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input 
                {...register('email')}
                type="email"
                defaultValue="admin@panchayatguard.gov.in"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
              />
              {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <input 
                  {...register('password')}
                  type={showPassword ? 'text' : 'password'}
                  defaultValue="SecurePassword123!"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
                />
                <button 
                  type="button" 
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded text-pg-blue focus:ring-pg-blue" defaultChecked />
                <span className="text-sm text-gray-600">Remember me</span>
              </label>
            </div>

            <button 
              type="submit"
              className="w-full bg-pg-navy text-white py-3 rounded-lg font-bold hover:bg-opacity-90 transition-colors flex items-center justify-center gap-2"
            >
              Sign In to Dashboard
            </button>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
               <p className="text-xs text-center text-gray-500 mb-3 font-semibold uppercase tracking-wider">Hackathon Jury Quick Access</p>
               <div className="grid grid-cols-2 gap-2">
                 <button type="button" onClick={() => onSubmit({email: 'admin@panchayatguard.gov.in', password: 'SecurePassword123!'})} className="text-xs py-2 bg-blue-50 text-pg-blue font-bold rounded border border-blue-100 hover:bg-blue-100 transition-colors">
                   Login as Admin
                 </button>
                 <button type="button" onClick={() => onSubmit({email: 'dm.vikram@gov.in', password: 'SecurePassword123!'})} className="text-xs py-2 bg-green-50 text-green-700 font-bold rounded border border-green-100 hover:bg-green-100 transition-colors">
                   Login as Official
                 </button>
               </div>
            </div>
          </form>"""

import re
content = re.sub(r'<form onSubmit=\{handleSubmit\(onSubmit\)\} className="space-y-6">.*', replacement + "\n        </div>\n      </div>\n    </div>\n  );\n}", content, flags=re.DOTALL)

with open('src/pages/Login.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
