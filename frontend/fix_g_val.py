with open('src/components/GrievanceModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add native required attributes so browser shows validation tooltips
content = content.replace("<input {...register('subject', { required: true })}", "<input required {...register('subject')} placeholder='Enter subject'")
content = content.replace("<textarea {...register('description', { required: true })}", "<textarea required {...register('description')} placeholder='Detailed description of the issue'")
content = content.replace("<select {...register('panchayat_id', { required: true })}", "<select required {...register('panchayat_id')}")
content = content.replace("<select {...register('category', { required: true })}", "<select required {...register('category')}")
content = content.replace("<input {...register('submitted_by', { required: true })}", "<input required {...register('submitted_by')} placeholder='Your Email or Name'")
content = content.replace("<select {...register('priority', { required: true })}", "<select required {...register('priority')}")

with open('src/components/GrievanceModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
