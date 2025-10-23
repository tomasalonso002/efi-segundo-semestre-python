# Activar la db
sudo systemctl stop mysql 
sudo systemctl stop nginx
sudo systemctl stop apache2

sudo /opt/lampp/lampp start


# Lineas para modificar la db y atualizar
alembic revision --autogenerate -m "Creando is_active en UseCrendetials"
alembic upgrade head


     try:
            data = PostSchema().load(request.json)
            post.id = data["id"]
            post.title = data["title"]
            post.content= data["content"]
            post.create_at = data["create_at"]
            post.autor = data["autor.name"]
            post.category = data["catrgory.type_category"]
            except ValidationError as err:
            return jsonify({
                "Error" : err.messages
            })

 
Parámetro	            Qué hace	                                     Ejemplo
dump_only=True	Solo aparece al devolver datos (no se acepta en entrada)	id
allow_none=True	Permite que el valor sea None	                      title, content
only=[...]	      Limita los campos mostrados en relaciones	              category
fields.Nested()	 Incluye otro esquema anidado	                     autor, category