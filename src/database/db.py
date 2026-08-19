from src.database.config import supabase
from datetime import datetime
import bcrypt



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 



def create_teacher(username, password, name):

    data = { "username" : username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = (
        supabase.table('subjects')
        .select("*, subject_students(count), attendance_logs(timestamp,is_present)")
        .eq("teacher_id", teacher_id)
        .order('created_at', desc=True)
        .execute()
    )
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions
        sub['total_attended'] = sum(1 for log in attendance if log.get('is_present'))

        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def update_student_avatar(student_id, avatar_value):
    response = supabase.table('students').update({'avatar': avatar_value}).eq('student_id', student_id).execute()
    return response.data


def get_students_in_subject(subject_id):
    # Same roster-fetch pattern used in teacher_screen.py's Run Face Analysis
    # (subject_students -> students(*) join), pulled out here so student-side
    # "beef mode" can reuse it instead of duplicating the raw query.
    response = supabase.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
    return response.data


def update_subject_note(student_id, subject_id, note_text):
    response = (
        supabase.table('subject_students')
        .update({'notes': note_text})
        .eq('student_id', student_id)
        .eq('subject_id', subject_id)
        .execute()
    )
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data


def create_dispute(student_id, subject_id, class_date, message):
    data = {
        'student_id': student_id,
        'subject_id': subject_id,
        'class_date': str(class_date),
        'student_message': message,
        'status': 'open',
    }
    response = supabase.table('attendance_disputes').insert(data).execute()
    return response.data


def get_disputes_for_student(student_id):
    response = (
        supabase.table('attendance_disputes')
        .select('*, subjects(name)')
        .eq('student_id', student_id)
        .order('created_at', desc=True)
        .execute()
    )
    return response.data


def get_disputes_for_teacher(teacher_id):
    # Same subjects!inner(...) teacher-scoping pattern as get_attendance_for_teacher.
    # 'open' sorts before 'resolved' alphabetically, so ordering by status
    # ascending puts open disputes first with no extra case logic needed.
    response = (
        supabase.table('attendance_disputes')
        .select("*, subjects!inner(*), students(name)")
        .eq('subjects.teacher_id', teacher_id)
        .order('status')
        .order('created_at', desc=True)
        .execute()
    )
    return response.data


def reply_to_dispute(dispute_id, reply_text):
    response = (
        supabase.table('attendance_disputes')
        .update({'teacher_reply': reply_text})
        .eq('dispute_id', dispute_id)
        .execute()
    )
    return response.data


def resolve_dispute(dispute_id):
    # Matches the naive-local timestamp convention already used for
    # attendance_logs.timestamp elsewhere in this codebase (see
    # student_screen.py's _parse_log_date), rather than introducing a lone
    # correctly-UTC-tagged timestamp column that would need different
    # parsing than every other date field in the app.
    response = (
        supabase.table('attendance_disputes')
        .update({'status': 'resolved', 'resolved_at': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")})
        .eq('dispute_id', dispute_id)
        .execute()
    )
    return response.data