with open('src/components/GrievanceModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the unstructured inputs with beautifully labeled ones.
new_form = """              <>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Subject</label>
                  <input required {...register('subject')} placeholder='e.g. Payment Delay for Solar Panels' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Description</label>
                  <textarea required {...register('description')} placeholder='Provide detailed explanation...' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" rows={3}></textarea>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Panchayat</label>
                  <select required {...register('panchayat_id')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                    <option value="">-- Select Panchayat --</option>
                    {panchayats.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700">Category</label>
                    <select required {...register('category')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                      <option value="Corruption">Corruption</option>
                      <option value="Delay">Delay</option>
                      <option value="Quality Issue">Quality Issue</option>
                      <option value="Missing Goods">Missing Goods</option>
                      <option value="Overpricing">Overpricing</option>
                      <option value="Contract Violation">Contract Violation</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700">Priority</label>
                    <select required {...register('priority')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                      <option value="Critical">Critical</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Submitted By</label>
                  <input required {...register('submitted_by')} placeholder='Your Email or Name' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" />
                </div>
              </>"""

import re
# The old block starts at `<>` and ends before `)}` and `<div className="flex justify-end gap-3 mt-6">`
# Let's just find the `</>` and replace everything inside.
content = re.sub(r'<>.*?</>', new_form, content, flags=re.DOTALL)

with open('src/components/GrievanceModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
