from flask import Blueprint, jsonify, request
from models import db, Post

blog_bp = Blueprint('blog', __name__)

# Listar posts públicos (opcionalmente filtrar por cliente)
@blog_bp.route('/posts', methods=['GET'])
def listar_posts():
    cliente_id = request.args.get('cliente_id')  # si se pasa, filtra por cliente
    query = Post.query.filter_by(publicado=True)
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    posts = query.order_by(Post.fecha_publicacion.desc()).all()
    return jsonify([p.to_dict() for p in posts])

# Ver un post por slug
@blog_bp.route('/posts/<slug>', methods=['GET'])
def ver_post(slug):
    post = Post.query.filter_by(slug=slug, publicado=True).first()
    if not post:
        return jsonify({'error': 'Post no encontrado'}), 404
    return jsonify(post.to_dict())