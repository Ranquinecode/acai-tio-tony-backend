from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Categoria, Produto, Pedido, ProdutoGrupoOpcao, ItemCombo, ItemGrupoOpcao
from .serializers import (
    CategoriaSerializer, 
    ProdutoSerializer, 
    PedidoSerializer
)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lista todas as categorias ativas trazendo produtos, grupos de opções,
    itens e combos pré-carregados na memória para alta performance.
    """
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        # Prefetch otimizado da relação intermediária de grupos por produto
        prefetch_produto_grupos = Prefetch(
            'produto_grupos',
            queryset=ProdutoGrupoOpcao.objects.select_related('grupo_opcao')
                .prefetch_related(
                    Prefetch(
                        'grupo_opcao__itens_relacionados',
                        queryset=ItemGrupoOpcao.objects.exclude(item__disponibilidade='oculto')
                            .select_related('item')
                            .prefetch_related('grupos_filhos__itens_relacionados__item')
                            .order_by('ordem')
                    )
                )
                .order_by('ordem')
        )

        # Prefetch otimizado de produtos dentro de combos
        prefetch_itens_combo = Prefetch(
            'itens_combo',
            queryset=ItemCombo.objects.select_related('produto_conteudo')
                .prefetch_related(
                    'produto_conteudo__produto_grupos__grupo_opcao__itens_relacionados__item',
                    'produto_conteudo__produto_grupos__grupo_opcao__itens_relacionados__grupos_filhos__itens_relacionados__item'
                )
                .order_by('ordem')
        )

        # Prefetch de produtos ativos na categoria
        prefetch_produtos = Prefetch(
            'produtos',
            queryset=Produto.objects.filter(ativo=True)
                .prefetch_related(prefetch_produto_grupos, prefetch_itens_combo)
        )

        return Categoria.objects.filter(ativo=True)\
            .prefetch_related(prefetch_produtos)\
            .order_by('ordem')


class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta direta de produtos ativos.
    """
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        prefetch_produto_grupos = Prefetch(
            'produto_grupos',
            queryset=ProdutoGrupoOpcao.objects.select_related('grupo_opcao')
                .prefetch_related(
                    Prefetch(
                        'grupo_opcao__itens_relacionados',
                        queryset=ItemGrupoOpcao.objects.exclude(item__disponibilidade='oculto')
                            .select_related('item')
                            .prefetch_related('grupos_filhos__itens_relacionados__item')
                            .order_by('ordem')
                    )
                )
                .order_by('ordem')
        )

        prefetch_itens_combo = Prefetch(
            'itens_combo',
            queryset=ItemCombo.objects.select_related('produto_conteudo')
                .prefetch_related(
                    'produto_conteudo__produto_grupos__grupo_opcao__itens_relacionados__item',
                    'produto_conteudo__produto_grupos__grupo_opcao__itens_relacionados__grupos_filhos__itens_relacionados__item'
                )
                .order_by('ordem')
        )

        return Produto.objects.filter(ativo=True)\
            .prefetch_related(prefetch_produto_grupos, prefetch_itens_combo)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


@api_view(['GET'])
def healthcheck(request):
    """Endpoint leve para manter a aplicação ativa via Cron-job"""
    return Response({"status": "ok", "message": "Açaí do Tio Tony API Online"})
