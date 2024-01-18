#!/bin/python3
import click
import sqlite3

DB_NAME = "academy.db"

def execute_query(query, values=None, fetchone=False):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    if fetchone:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

# CLI commands
@click.group()
def cli():
    pass


@cli.command()
def create_tables():
    queries = [
        "CREATE TABLE IF NOT EXISTS study_groups (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER);",
        "CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY, name TEXT);",
        "CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, name TEXT);",
        "CREATE TABLE IF NOT EXISTS lectures (id INTEGER PRIMARY KEY, group_id INTEGER, teacher_id INTEGER, discipline TEXT, lectures_count INTEGER);",
    ]

    for query in queries:
        execute_query(query)

    click.echo("Tables created successfully.")





# Study Groups commands
@cli.command()
@click.option("--name", prompt="Enter the study group name", help="Name of the study group")
@click.option("--department-id", prompt="Enter the department ID", type=int, help="ID of the department to which the group belongs")
def insert_study_group(name, department_id):
    query = "INSERT INTO study_groups (name, department_id) VALUES (?, ?);"
    execute_query(query, (name, department_id))
    click.echo(f"Study group '{name}' inserted successfully.")

@cli.command()
@click.option("--group-id", prompt="Enter the group ID", type=int, help="ID of the study group to update")
@click.option("--new-name", prompt="Enter the new name", help="New name for the study group")
def update_study_group(group_id, new_name):
    query = "UPDATE study_groups SET name = ? WHERE id = ?;"
    execute_query(query, (new_name, group_id))
    click.echo(f"Study group with ID {group_id} updated successfully.")

@cli.command()
@click.option("--group-id", prompt="Enter the group ID", type=int, help="ID of the study group to delete")
def delete_study_group(group_id):
    query = "DELETE FROM study_groups WHERE id = ?;"
    execute_query(query, (group_id,))
    click.echo(f"Study group with ID {group_id} deleted successfully.")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_study_groups(output):
    query = "SELECT * FROM study_groups;"
    result = execute_query(query)

    if output == 'print':
        click.echo("Study Groups:")
        for row in result:
            click.echo(f"ID: {row[0]}, Name: {row[1]}, Department ID: {row[2]}")
    elif output == 'file':
        with open('study_groups_report.txt', 'w') as file:
            file.write("Study Groups:\n")
            for row in result:
                file.write(f"ID: {row[0]}, Name: {row[1]}, Department ID: {row[2]}\n")





# Teachers commands
@cli.command()
@click.option("--name", prompt="Enter the teacher name", help="Name of the teacher")
def insert_teacher(name):
    query = "INSERT INTO teachers (name) VALUES (?);"
    execute_query(query, (name,))
    click.echo(f"Teacher '{name}' inserted successfully.")

@cli.command()
@click.option("--teacher-id", prompt="Enter the teacher ID", type=int, help="ID of the teacher to update")
@click.option("--new-name", prompt="Enter the new name", help="New name for the teacher")
def update_teacher(teacher_id, new_name):
    query = "UPDATE teachers SET name = ? WHERE id = ?;"
    execute_query(query, (new_name, teacher_id))
    click.echo(f"Teacher with ID {teacher_id} updated successfully.")

@cli.command()
@click.option("--teacher-id", prompt="Enter the teacher ID", type=int, help="ID of the teacher to delete")
def delete_teacher(teacher_id):
    query = "DELETE FROM teachers WHERE id = ?;"
    execute_query(query, (teacher_id,))
    click.echo(f"Teacher with ID {teacher_id} deleted successfully.")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_teachers(output):
    query = "SELECT * FROM teachers;"
    result = execute_query(query)

    if output == 'print':
        click.echo("Teachers:")
        for row in result:
            click.echo(f"ID: {row[0]}, Name: {row[1]}")
    elif output == 'file':
        with open('teachers_report.txt', 'w') as file:
            file.write("Teachers:\n")
            for row in result:
                file.write(f"ID: {row[0]}, Name: {row[1]}\n")








# Departments commands
@cli.command()
@click.option("--name", prompt="Enter the department name", help="Name of the department")
def insert_department(name):
    query = "INSERT INTO departments (name) VALUES (?);"
    execute_query(query, (name,))
    click.echo(f"Department '{name}' inserted successfully.")

@cli.command()
@click.option("--dept-id", prompt="Enter the department ID", type=int, help="ID of the department to update")
@click.option("--new-name", prompt="Enter the new name", help="New name for the department")
def update_department(dept_id, new_name):
    query = "UPDATE departments SET name = ? WHERE id = ?;"
    execute_query(query, (new_name, dept_id))
    click.echo(f"Department with ID {dept_id} updated successfully.")

@cli.command()
@click.option("--dept-id", prompt="Enter the department ID", type=int, help="ID of the department to delete")
def delete_department(dept_id):
    query = "DELETE FROM departments WHERE id = ?;"
    execute_query(query, (dept_id,))
    click.echo(f"Department with ID {dept_id} deleted successfully.")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_departments(output):
    query = "SELECT * FROM departments;"
    result = execute_query(query)

    if output == 'print':
        click.echo("Departments:")
        for row in result:
            click.echo(f"ID: {row[0]}, Name: {row[1]}")
    elif output == 'file':
        with open('departments_report.txt', 'w') as file:
            file.write("Departments:\n")
            for row in result:
                file.write(f"ID: {row[0]}, Name: {row[1]}\n")









# Reporting commands

@cli.command()
@click.option("--group-id", prompt="Enter the group ID", type=int, help="ID of the study group")
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_teachers_for_group(group_id, output):
    query = """
    SELECT teachers.name
    FROM teachers
    JOIN lectures ON teachers.id = lectures.teacher_id
    WHERE lectures.group_id = ?;
    """
    result = execute_query(query, (group_id,))

    if output == 'print':
        click.echo(f"Teachers giving lectures to group {group_id}:")
        for row in result:
            click.echo(f"Name: {row[0]}")
    elif output == 'file':
        with open(f'teachers_for_group_{group_id}_report.txt', 'w') as file:
            file.write(f"Teachers giving lectures to group {group_id}:\n")
            for row in result:
                file.write(f"Name: {row[0]}\n")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_departments_and_groups(output):
    query = """
    SELECT departments.name AS department, study_groups.name AS group_name
    FROM departments
    LEFT JOIN study_groups ON departments.id = study_groups.department_id;
    """
    result = execute_query(query)

    if output == 'print':
        click.echo("Department names and group names:")
        for row in result:
            click.echo(f"Department: {row[0]}, Group: {row[1]}")
    elif output == 'file':
        with open('departments_and_groups_report.txt', 'w') as file:
            file.write("Department names and group names:\n")
            for row in result:
                file.write(f"Department: {row[0]}, Group: {row[1]}\n")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_department_with_most_groups(output):
    query = """
    SELECT departments.name
    FROM departments
    WHERE id = (
        SELECT department_id
        FROM study_groups
        GROUP BY department_id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    );
    """
    result = execute_query(query)

    if output == 'print':
        click.echo(f"Department with the largest number of groups: {result[0][0]}")
    elif output == 'file':
        with open('department_with_most_groups_report.txt', 'w') as file:
            file.write(f"Department with the largest number of groups: {result[0][0]}\n")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_department_with_least_groups(output):
    query = """
    SELECT departments.name
    FROM departments
    WHERE id = (
        SELECT department_id
        FROM study_groups
        GROUP BY department_id
        ORDER BY COUNT(*) ASC
        LIMIT 1
    );
    """
    result = execute_query(query)

    if output == 'print':
        click.echo(f"Department with the smallest number of groups: {result[0][0]}")
    elif output == 'file':
        with open('department_with_least_groups_report.txt', 'w') as file:
            file.write(f"Department with the smallest number of groups: {result[0][0]}\n")

@cli.command()
@click.option("--teacher-id", prompt="Enter the teacher ID", type=int, help="ID of the teacher")
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_academic_disciplines_by_teacher(teacher_id, output):
    query = """
    SELECT DISTINCT lectures.discipline
    FROM lectures
    WHERE lectures.teacher_id = ?;
    """
    result = execute_query(query, (teacher_id,))

    if output == 'print':
        click.echo(f"Academic disciplines taught by teacher {teacher_id}:")
        for row in result:
            click.echo(f"Discipline: {row[0]}")
    elif output == 'file':
        with open(f'academic_disciplines_by_teacher_{teacher_id}_report.txt', 'w') as file:
            file.write(f"Academic disciplines taught by teacher {teacher_id}:\n")
            for row in result:
                file.write(f"Discipline: {row[0]}\n")

@cli.command()
@click.option("--discipline", prompt="Enter the discipline name", help="Name of the discipline")
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_departments_by_discipline(discipline, output):
    query = """
    SELECT DISTINCT departments.name
    FROM departments
    JOIN study_groups ON departments.id = study_groups.department_id
    JOIN lectures ON study_groups.id = lectures.group_id
    WHERE lectures.discipline = ?;
    """
    result = execute_query(query, (discipline,))

    if output == 'print':
        click.echo(f"Departments for discipline {discipline}:")
        for row in result:
            click.echo(f"Department: {row[0]}")
    elif output == 'file':
        with open(f'departments_by_discipline_{discipline}_report.txt', 'w') as file:
            file.write(f"Departments for discipline {discipline}:\n")
            for row in result:
                file.write(f"Department: {row[0]}\n")

@cli.command()
@click.option("--sub-department-id", prompt="Enter the sub-department ID", type=int, help="ID of the sub-department")
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_group_names_by_sub_department(sub_department_id, output):
    query = """
    SELECT study_groups.name
    FROM study_groups
    WHERE study_groups.department_id = ?;
    """
    result = execute_query(query, (sub_department_id,))

    if output == 'print':
        click.echo(f"Group names for sub-department {sub_department_id}:")
        for row in result:
            click.echo(f"Group: {row[0]}")
    elif output == 'file':
        with open(f'group_names_by_sub_department_{sub_department_id}_report.txt', 'w') as file:
            file.write(f"Group names for sub-department {sub_department_id}:\n")
            for row in result:
                file.write(f"Group: {row[0]}\n")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_disciplines_and_teachers_with_most_lectures(output):
    query = """
    SELECT lectures.discipline, teachers.name
    FROM lectures
    JOIN teachers ON lectures.teacher_id = teachers.id
    WHERE lectures.lectures_count = (
        SELECT MAX(lectures_count)
        FROM lectures
    );
    """
    result = execute_query(query)

    if output == 'print':
        click.echo("Disciplines and teachers with the most lectures:")
        for row in result:
            click.echo(f"Discipline: {row[0]}, Teacher: {row[1]}")
    elif output == 'file':
        with open('disciplines_and_teachers_with_most_lectures_report.txt', 'w') as file:
            file.write("Disciplines and teachers with the most lectures:\n")
            for row in result:
                file.write(f"Discipline: {row[0]}, Teacher: {row[1]}\n")

@cli.command()
@click.option("--output", type=click.Choice(['print', 'file']), default='print', help="Output method: print or file")
def report_discipline_with_least_lectures(output):
    query = """
    SELECT discipline
    FROM lectures
    GROUP BY discipline
    ORDER BY SUM(lectures_count) ASC
    LIMIT 1;
    """
    result = execute_query(query)

    if output == 'print':
        click.echo(f"Discipline with the least number of lectures: {result[0][0]}")
    elif output == 'file':
        with open('discipline_with_least_lectures_report.txt', 'w') as file:
            file.write(f"Discipline with the least number of lectures: {result[0][0]}\n")
@cli.command()
@click.option("--group-id", prompt="Enter the group ID", type=int, help="ID of the study group")
@click.option("--teacher-id", prompt="Enter the teacher ID", type=int, help="ID of the teacher")
@click.option("--discipline", prompt="Enter the discipline", help="Academic discipline")
@click.option("--lectures-count", prompt="Enter the number of lectures", type=int, help="Number of lectures")
def assign_teacher_to_group(group_id, teacher_id, discipline, lectures_count):
    query = "INSERT INTO lectures (group_id, teacher_id, discipline, lectures_count) VALUES (?, ?, ?, ?);"
    execute_query(query, (group_id, teacher_id, discipline, lectures_count))
    click.echo(f"Teacher with ID {teacher_id} assigned to group {group_id} for discipline {discipline} successfully.")


if __name__ == "__main__":
    cli()