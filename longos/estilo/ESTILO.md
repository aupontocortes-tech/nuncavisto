# Estilo aprovado dos vídeos longos (insetos v8, 25/11/2026)

Thiago aprovou. Os próximos vídeos longos devem seguir este padrão.

## Roteiro
- Abre com a cena mais impactante no 1º segundo.
- Em seguida apresenta rapidinho o que vai mostrar: uma frase por assunto, cada uma com a imagem do próprio assunto.
- Narração explicativa: o "como" e o "porquê", com números verificados.
- Final curto no ÚLTIMO assunto, com uma frase só (pergunta pro comentário + inscrição). Nunca voltar pro começo nem repetir bicho.

## Imagem
- Vídeo real (archive.org / figshare, licença livre) + fotos reais do iNaturalist (CC BY / CC0, `inat.py`), com crédito na descrição.
- Foto vira clipe de 6 s com zoom lento e fundo desfocado (`fclip.py`).
- Cortes de 1,8 a 2,8 s, alternando vídeo e foto. Nunca repetir o mesmo trecho (`rl.py --dry` mostra as repetições).
- Vídeo fraco (mato, bicho minúsculo) com limite de tempo.
- Uma ilustração por assunto, de 6 a 8 s, só onde explica algo (`ill.py` / `ill2.py`).

## Som e tela
- Voz Antonio -5%, com pausas escritas no texto ("…" e vírgulas), sintetizada por parágrafo (`tts2.py`).
- Trilha Kevin MacLeod com ducking. Whoosh só em troca de capítulo ou entrada/saída de ilustração.
- Caixa de impacto no canto superior direito, nunca em cima do bicho. Selo do capítulo no canto superior esquerdo. Legenda palavra por palavra.

## Ordem
mk.py → tts2.py → inat.py + fclip.py → rl.py --dry (conferir) → go.sh → conferir ~30 quadros → mandar pro Thiago aprovar → publicar.
