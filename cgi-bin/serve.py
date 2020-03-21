#!/usr/bin/python

print "Content-type: text/html"
print

# Pane see programm kataloogi /home/kasutajanimi/public_html/cgi-bin
# ja ytle samas kasurealt
# chmod a+rx serve.py

# See programm laheb kaima, kui avad urli
# http://dijkstra.cs.ttu.ee/~kasutajanimi/cgi-bin/serve.py

# kasutame neid pythonisse sisse ehitatud standardteeke

import sqlite3
import json  
import cgi
import cgitb

# see annab debugimiseks arusaadavaid veateateid brauserile
cgitb.enable()

# sinu programm, mis pannakse paringu peale kaima

def getdata():
   	
  args = cgi.FieldStorage()
  # vaata, kas urlil anti key, op ja val parameetrid
  key=args.getvalue("key",'')
  op=args.getvalue("op",'')
  val=args.getvalue("val",'') 
  # vota baasiga yhendust, valmista ette paring
  conn = sqlite3.connect('data.db')
  cur = conn.cursor()
  
  # hakka kokku panema paringu-sqli, alustades standardosast
  sql="""select Perenimi,Eesnimi,Asutus,Ametikoht,aasta,arvestuslikpalk from maintable"""
  # kui olid olemas key, op ja val, siis ehita where tingimus
  if key and val:
    if not op: # vaikimisi olgu op =
      op = "="
    # kontrollime, kas parameetrid ok  
    if (not (key in ["id","Asutus","Stryksus","Allstrukt","Ametikoht","Eesnimi","Perenimi","arvestuslikpalk","aasta","keskm"]) 
        or
        not (op in ["=","<",">","!="])):
      # valed parameetrid, sulge yhendus
      cur.close()
      conn.close()
      # anna veateade ja lopeta
      return('"error"')
    # siin koik ok
    where = " where " + key + op + "?"
    args = [val]
  else:
    where=""
    args=None
    
  # liida where tingimus sql standardosale
  sql = sql + where
  #liida sql lausele sorteering
  if key == "arvestuslikpalk":
    sql="""select Perenimi,Eesnimi,Asutus,Ametikoht,aasta,arvestuslikpalk from maintable"""
    where = " where " + key + '>' + "?"
    sql = sql + where
    sql = sql + " order by arvestuslikpalk desc "
    where = " where " + key + '>' + "?"
  else:  
    sql = sql + " order by Perenimi asc, Eesnimi asc, aasta desc "
    
  # tee paring baasi
  if args:
    cur.execute(sql,args)
  else:
    cur.execute(sql)
    
  # loe koik read sisse, mis paringuga klapivad
  res=cur.fetchall()
  # sulge yhendus
  cur.close()
  conn.close()
  
  # teisenda saadud tulemus json formaati ja anna vastuseks
  print(json.dumps(res))

# see paneb tegelikult programmi algul kaima:

getdata()
