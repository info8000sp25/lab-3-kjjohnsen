import random
import os

def generate_enrollment_data_v4(program_name="INFO", num_courses=20, num_students=200, courses_per_student_range=(1, 5), withdrawal_rate_range=(0, 0.20), output_dir="enrollment_data_v4"):
    """
    Generates student enrollment data with course withdrawals and shuffled student IDs.

    Args:
        program_name: The name of the degree program.
        num_courses: The total number of courses offered.
        num_students: The total number of students.
        courses_per_student_range: (min, max) courses per student.
        withdrawal_rate_range: (min, max) percentage of withdrawals.
        output_dir: Directory to save the files.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate student IDs
    student_ids = []
    while len(student_ids) < num_students:
        new_id = random.randint(10000000, 99999999)
        if new_id not in student_ids:
            student_ids.append(new_id)

    # Shuffle student IDs *before* assigning courses
    random.shuffle(student_ids)

    # 2. Generate number of courses taken
    num_courses_taken = [random.randint(courses_per_student_range[0], courses_per_student_range[1]) for _ in range(num_students)]

    # 3. Generate course numbers
    course_numbers = []
    while len(course_numbers) < num_courses:
        new_course_num = random.randint(1000, 9999)
        if new_course_num not in course_numbers:
          course_numbers.append(new_course_num)
    course_numbers.sort()

    # 4. Create course enrollments (initially empty)
    course_enrollments = {f"{program_name}{course_num}": [] for course_num in course_numbers}

    # 5. Assign students to courses
    for i, student_id in enumerate(student_ids):
        num_courses_for_student = num_courses_taken[i]
        selected_course_indices = random.sample(range(num_courses), num_courses_for_student)
        for course_index in selected_course_indices:
            course_name = f"{program_name}{course_numbers[course_index]}"
            course_enrollments[course_name].append(student_id)

    # 6. Simulate withdrawals and write to files
    for course_name, enrolled_students in course_enrollments.items():
        filepath = os.path.join(output_dir, f"{course_name}.txt")
        withdrawal_rate = random.uniform(withdrawal_rate_range[0], withdrawal_rate_range[1])
        num_withdrawals = int(len(enrolled_students) * withdrawal_rate)
        withdrawn_students = random.sample(enrolled_students, num_withdrawals)
        remaining_students = [sid for sid in enrolled_students if sid not in withdrawn_students]

        with open(filepath, "w") as f:
            f.write(f"{num_withdrawals}\n")
            for student_id in sorted(remaining_students):
                f.write(f"{student_id}\n")
            for student_id in sorted(withdrawn_students):
                f.write(f"{student_id}\n")

    # 7. Create student-course summary
    summary_filepath = os.path.join(output_dir, "student_courses_summary.txt")
    with open(summary_filepath, "w") as f:
        f.write("StudentID,Courses\n")
        for i, student_id in enumerate(student_ids):
            courses_taken = []
            for course_name, enrolled_students in course_enrollments.items():
                filepath = os.path.join(output_dir, f"{course_name}.txt")
                with open(filepath, 'r') as course_file:
                    num_withdrawals = int(course_file.readline().strip())
                    # Read *all* student IDs from the file
                    all_students_in_file = [int(line.strip()) for line in course_file]
                    #Check to ensure student didn't withdraw.
                    if student_id in all_students_in_file[:len(all_students_in_file) - num_withdrawals]:
                        courses_taken.append(course_name)
            f.write(f"{student_id},{','.join(sorted(courses_taken))}\n")

    print(f"Data generated and saved to: {output_dir}")



def generate_student_course_matrix_v4(program_name="INFO", num_courses=20, output_dir="enrollment_data_v4"):
    """Generates student-course matrix, accounting for withdrawals."""

    if not os.path.exists(output_dir):
        print(f"Error: Directory '{output_dir}' not found. Run generate_enrollment_data_v4 first.")
        return

    course_numbers = []
    for filename in os.listdir(output_dir):
        if filename.startswith(program_name) and filename.endswith(".txt"):
            course_numbers.append(filename[len(program_name):-4])
    course_numbers = sorted([int(c) for c in course_numbers])


    student_ids = []
    summary_filepath = os.path.join(output_dir, 'student_courses_summary.txt')
    with open(summary_filepath, 'r') as file:
        next(file) #skip header
        for line in file:
            student_id, _ = line.strip().split(',', 1)
            student_ids.append(int(student_id))
    student_ids.sort()


    matrix_filepath = os.path.join(output_dir, "student_course_matrix.csv")
    with open(matrix_filepath, "w") as outfile:
        header = "StudentID," + ",".join([f"{program_name}{c}" for c in course_numbers])
        outfile.write(header + "\n")

        for student_id in student_ids:
            row = [str(student_id)]
            for course_num in course_numbers:
                course_filepath = os.path.join(output_dir, f"{program_name}{course_num}.txt")
                with open(course_filepath, "r") as infile:
                    num_withdrawals = int(infile.readline().strip())
                    all_students_in_file = [int(line.strip()) for line in infile]
                    remaining_students = all_students_in_file[:len(all_students_in_file)-num_withdrawals]
                    row.append('1' if student_id in remaining_students else '0')
            outfile.write(",".join(row) + "\n")
    print(f"Student-course matrix saved to: {matrix_filepath}")



# Example Usage:
generate_enrollment_data_v4(num_courses=5, num_students=150, courses_per_student_range=(1, 5), withdrawal_rate_range=(0.05, 0.15), output_dir="enrollment_data_v4")