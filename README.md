

#AUTENTICACION
1) INSTANCIAR LA BASE DE DATOS
Ejecutar el comando en la terminal:

python creted_db.py

1) REGISTER
methods: post
http://127.0.0.1:5000/register
Ejemplo body:
{
  "name":"Martin Alonso",
  "email":"martin@gmail.com",
  "role":"user",
  "password":"martin123"
}

{
  "name":"admin",
  "email":"admin@gmail.com",
  "role":"admin",
  "password":"admin123"
}

{
  "name":"Jose Rodriguez",
  "email":"jose@gmail.com",
  "role":"moderador",
  "password":"jose123"
}

2) LOGIN
methods: post
http://127.0.0.1:5000/login
Ejemplo body:

{
  "email":"Marin@gmail.com",
  "password":"martin123"
}

3) CATEGORIAS
methods: post
http://127.0.0.1:5000/categories
Ejemplo body:
{
  "type_category":"Futbol"
}

methods: get
Listado de categorias

4) Post
methods: post
http://127.0.0.1:5000/post
Ejemplo body:
{
  "title":"El domingo gano atenasss",
  "content":"Le gano 1 a 0 Sarmiento la banda",
  "user_id": 3,
  "category_id":1
}

methods: get
http://127.0.0.1:5000/post

methods: get
http://127.0.0.1:5000/post/1

methods: patch (eliminar)
http://127.0.0.1:5000/post/1

methods: put (editar)
http://127.0.0.1:5000/post/1
Ejemplo body:
{
  "title":"El domingo paso atenasss",
  "content":"Le gano 1 a 0 Sarmiento la banda y juega los cuartos de final",
  "user_id": 3,
  "category_id":1
}

5) Comentarios
methods: post
http://127.0.0.1:5000/post/1/comment
Ejemplo de body:
{
  "text_comment":"Que bueno",
  "user_id": 2
}

methods: get
http://127.0.0.1:5000/post/1/comment

methods: patch (elimianar)
http://127.0.0.1:5000/post/comment/1

Pruebas de Error:

Con el usuario:
http://127.0.0.1:5000/login

body:
{
"email":"martin@gmail.com",
"password":"martin123"
}

En la ruta:
http://127.0.0.1:5000/categories
methods: post
body:
{
  "type_category":"Automovilismo"
}
Return esperado: "Error": "Rol no autorizado"
Con el usuario
{  
"email":"admin@gmail.com",
"password":"admin123"
}
En la misma ruta cambiando el token
Return Esperado: "message": "Categoria creada con exito"


Listar mis post:

http://127.0.0.1:5000/my_post
method: get

Si el usurio login tiene post creados y activos te los trae, sino 'Error' : 'NO hay post'

Listar todos los post:

http://127.0.0.1:5000/posts
method: get

Esta ruta tiene que retornar todos los activos de todos los usuarios, no requiere estar login

Eliminar post:

http://127.0.0.1:5000/post/<id>
method: patch

Solo podras eliminar este post si sos el duño del post o si tenes un rol de moderado o admin
Si todo sale bien: "Post borrado"
Si no sale bien: "No estas autorizado a borrar este post" o  "No se encontro el post"

Editar post:

http://127.0.0.1:5000/post/<id>
method: put

body:
{
  "title":"El domingo paso atenasss",
  "content":"Le gano 1 a 0 Sarmiento la banda",
  "user_id": 59,
  "category_id":1
}

Solo pueden editar el post si sos el dueño del post o si tenes un rol de moderador o admin
Si sale todo bien: "Posteo editado correctamente"
Si todo sale mal: "No se encontro el post" o  "No estas autorizado a editar este post"



