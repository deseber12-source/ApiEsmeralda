from flask import Blueprint, jsonify, request
from models import db, Post

blog_bp = Blueprint('blog', __name__)

# Listar posts públicos (opcionalmente filtrar por cliente)
@blog_bp.route('/posts', methods=['GET'])
def listar_posts():
    cliente_id = request.args.get('cliente_id')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 6, type=int)
    search = request.args.get('q', '').strip()

    query = Post.query.filter_by(publicado=True)
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    if search:
        query = query.filter(
            (Post.titulo.ilike(f'%{search}%')) |
            (Post.resumen.ilike(f'%{search}%')) |
            (Post.contenido.ilike(f'%{search}%'))
        )

    # Paginación
    paginated = query.order_by(Post.fecha_publicacion.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )

    return jsonify({
        'posts': [p.to_dict() for p in paginated.items],
        'total': paginated.total,
        'page': page,
        'pages': paginated.pages,
        'per_page': limit
    })

# Ver un post por slug
@blog_bp.route('/posts/<slug>', methods=['GET'])
def ver_post(slug):
    post = Post.query.filter_by(slug=slug, publicado=True).first()
    if not post:
        return jsonify({'error': 'Post no encontrado'}), 404
    return jsonify(post.to_dict())