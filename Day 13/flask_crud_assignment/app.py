from flask import Flask,request,jsonify
from flask import jsonify
from pydantic import BaseModel
import psycopg2

app=Flask(__name__)

students=[]

def get_connection():
    conn=psycopg2.connect(
    host="localhost",
    database="students",
    user="postgres",
    password="Admin@123"
    )
    print("Connected to PostgresSQL successfully")
    return conn


class Student(BaseModel):
    id:int
    name:str
    course:str
    score:int


@app.route("/students", methods=['GET'])
def get_students():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
    """ SELECT * from students""")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)

@app.route("/students/<int:student_id>",methods=["GET"])
def get_student(student_id):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """SELECT * FROM students WHERE id=%s""",
        (student_id,)
    )

    row=cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(row)



@app.route("/students",methods=['POST'])
def create_student():
    data=request.get_json()
    student=Student(**data)
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """INSERT INTO students 
        (id,name,course,score)
        VALUES (%s,%s,%s,%s)""",
        (student.id,student.name,student.course,student.score)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "message":"Student created successfully",
    }),201

@app.route("/students/<int:student_id>",methods=['PUT'])
def update_student(student_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        UPDATE students SET score =%s where id=%s""",
        (4567,student_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"Updated Successfully"}),404


@app.route("/students/<int:student_id>",methods=['DELETE'])
def delete_student(student_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """DELETE FROM students WHERE id=%s""",
        (student_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"Student Deleted Successfully"}),404

if __name__ == "__main__":
    app.run(debug=True)





