from typing import Optional
from fastapi import FastAPI , Request
import uvicorn
import json
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins= [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add1")
async def add_1(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    if (body['statut'])=="chef":
        i="numcin_chef"
    else:
        i="numcin_chomeur"
    try:
        
        cursor.execute(f"INSERT INTO `{body['statut']}` ({i},`nom`,`prenom`,`numtel`,`sexe`,`datedenaissance`,`email`,`password`) VALUES ( '{body['cin']}' , '{body['nom']}' , '{body['prenom']}' , '{body['numtel']}' , '{body['gender']}' ,date '{body['dn']}','{body['email']}','{body['password']}');")
        db.commit()
        return{"ok"}
    except:
        db.rollback()
        return{"not ok"}

@app.post("/add2")
async def add_2(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    if (body['statut'])=="chef":
        i="numcin_chef"
    else:
        i="numcin_chomeur"

    try:
        cursor.execute(f"UPDATE `{body['statut']}` set nom_buisness='{body['nom_buisness']}',domaine_travail='{body['domaine']}',numtel_travail='{body['numtel_travail']}',adresse='{body['adresse']}' where {i}='{body['cin']}' ;")
        db.commit()
        return{"ok"}
    except:
        db.rollback()
        return{"not ok"}

@app.post("/add3")
async def add_3(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    
    try:
        cursor.execute(f"UPDATE `chomeur` set niveau_education='{body['niveau']}',specialite='{body['sp']}',langue='{body['lng']}',ajouter='{body['texte']}' where numcin_chomeur='{body['cin']}';")
        db.commit()
        return{"ok"}
    except:
        db.rollback()
        return{"not ok"}


@app.post("/searchchef")
async def search_chef(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    try:
        if((body['region']=="undefined")and(body['dom']=="undefined")):
            cursor.execute(f"select * from `chef` ;")
            row_headers=[ x[0] for x in cursor.description]
            ret=cursor.fetchall()
            json_data=[]
            for result in ret:
                json_data.append(dict(zip(row_headers,result)))
            return json_data
        else:
            cursor.execute(f"select * from `chef` where adresse='{body['region']}' AND domaine_travail='{body['dom']}' ;")
            row_headers=[ x[0] for x in cursor.description]
            ret=cursor.fetchall()
            json_data=[]
            for result in ret:
                json_data.append(dict(zip(row_headers,result)))
            return json_data
    except:
        return{"problem"}

@app.post("/login")
async def login_user(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    try:
        cursor.execute(f"select password from `{body['statut']}` where email='{body['email']}';")
        pwd=cursor.fetchone()
        return({"data":pwd})
    except:
        return({"data":"problem"})

@app.post("/searchchom")
async def search_chef(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    
    try:
        if((body['region']=="undefined")and(body['dom']=="undefined")):
            cursor.execute(f"select * from `chomeur` ;")
            row_headers=[ x[0] for x in cursor.description]
            ret=cursor.fetchall()
            json_data=[]
            for result in ret:
                json_data.append(dict(zip(row_headers,result)))
            return json_data
        else:
            cursor.execute(f"select * from `chomeur` where adresse='{body['region']}' AND domaine_travail='{body['dom']}' ;")
            row_headers=[ x[0] for x in cursor.description]
            ret=cursor.fetchall()
            json_data=[]
            for result in ret:
                json_data.append(dict(zip(row_headers,result)))
            return json_data
    except:
        return{"problem"}

@app.post("/delete_user")
async def delete_user(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    try:
        cursor.execute(f"delete from `{body['statut']}` where email='{body['email']}' ;")
        db.commit()
        return("user deleted successfully !")
    except:
        db.rollback()
        return("problem on delete !")

@app.post("/profil")
async def get_profile(request : Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    try:
        cursor.execute(f"select * from `{body['statut']}` where email='{body['email']}';")
        row_headers=[ x[0] for x in cursor.description]
        ret=cursor.fetchall()
        json_data=[]
        for result in ret:
            json_data.append(dict(zip(row_headers,result)))
        return json_data
    except:
        return{"problem"}

@app.post("/update")
async def update_user(request:Request):
    db=mysql.connector.connect(host="localhost", user="baha", password="baha0000", database="dreamjob")
    cursor=db.cursor() 
    body=json.loads(await request.body())
    try:
        
        if body['statut']=="chomeur":
            cursor.execute(f"UPDATE `chomeur` set email='{body['email']}',nom='{body['nom']}',prenom='{body['prenom']}',datedenaissance='{body['dn']}',numcin_chomeur='{body['cin']}',password='{body['password']}',numtel='{body['numtel']}',sexe='{body['gender']}',niveau_education='{body['niveau']}',specialite='{body['specialite']}',ajouter='{body['ajouter']}',nom_buisness='{body['nom_buisness']}',domaine_travail='{body['domaine']}',numtel_travail='{body['tel_travail']}',adresse='{body['adresse']}' where email='{body['anc_email']}';")
            db.commit()
            return{"ok"}
        else:
            cursor.execute(f"UPDATE `chef` set email='{body['email']}',nom='{body['nom']}',prenom='{body['prenom']}',datedenaissance='{body['dn']}',numcin_chef='{body['cin']}',password='{body['password']}',numtel='{body['numtel']}',sexe='{body['gender']}',nom_buisness='{body['nom_buisness']}',domaine_travail='{body['domaine']}',adresse='{body['adresse']}',numtel_travail='{body['tel_travail']}'  where email='{body['anc_email']}';")
            db.commit()
            return{"ok"}
    except:
        db.rollback()
        return{"not ok"}





