

#AUTENTICACION

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



