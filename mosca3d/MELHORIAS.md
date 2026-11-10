# Série 3D "Já pensou em como é ser um...?" — o que melhorar (feedback do Thiago, 09/11/2026)

Teste 1: mosca (1min37). Thiago: "ficou muito bom, qualidade ótima, mas pode melhorar". Ainda NÃO publicado.

## O que o Thiago pediu
1. **Pessoa de verdade com o chinelo**: mostrar o humano (corpo, braço levantando o chinelo), não só o chinelo flutuando.
2. **Lógica da cena**: ninguém bate o chinelo em cima de um bolo. A mosca tem que estar na mesa/parede/pia quando o chinelo vem, não em cima da comida.
3. **Mostrar o que é falado, em detalhe**: quando fala das almofadas peludas e grudentas das patas, MOSTRAR a pata de perto (zoom nos pelos, nas almofadas grudando no teto). Não só narrar.
4. **Ambiente com detalhes**: cozinha mais viva (objetos, migalhas, pia, azulejo, luz da janela), a pessoa que bate, coisas mínimas que dão realismo.
5. **Pequenos detalhes fazem a diferença**: ex. no vídeo da barata do @CriamosAssim ela se espreme na fresta e o corpo "desmonta" mostrando as placas. Cada "Esse é o seu ___" precisa de uma animação que MOSTRA o mecanismo.

## O que os vídeos de referência fazem (@CriamosAssim: lagartixa, escorpião, barata)
- Cada mecanismo tem um plano próprio em close + uma animação didática (língua lambendo o olho, cauda soltando, corpo achatando, pelos microscópicos).
- **Zoom em escala**: régua na tela indo de 1 cm → 0,1 mm → 0,01 mm → 0,000001 mm, entrando na pata até os pelos/espátulas.
- Infográficos ligados ao objeto: pílula branca com bolinha vermelha apontando a parte ("• LÍNGUA", "• ESPÁTULAS"), palavra riscada ("~~COLA~~ ~~VENTOSA~~"), relógio digital (03:12), calendário (1 DIA), velocímetro (100 KM/H).
- Personagem humano low poly (camiseta azul, chinelo azul gigante), luz da cozinha acendendo.
- Cenas trocam a cada 2-4 s com câmera sempre se mexendo.

## Técnica (para não demorar de novo)
- O render realista (Cycles) no GitHub levou ~7 h. Próximos: usar EEVEE no PC do Thiago com placa de vídeo (20-40 min) ou cenas mais leves no GitHub (menos desfoque/samples, 720p).
- Modelo da mosca: "housefly rigged" (Casuallboy55, CC BY) — crédito na descrição.

## Análise do vídeo da barata do @CriamosAssim x o nosso (09/11/2026) — Thiago não gostou da nossa barata v1
Medido: o deles tem ~46 cortes em 2min26 (1 a cada ~3 s); o nosso teve 4 em 1min32.
O que eles fazem e o nosso não fez:
- Troca de plano a cada frase (às vezes 2 por frase): close, plano aberto, de cima, de baixo, por dentro do corpo.
- Cenário muda: floresta de 300 milhões de anos, cozinha, fresta do azulejo, rua à noite, embaixo do pé.
- Letra/infográfico em quase todo plano: "300 MILHÕES DE ANOS", calendário "1 DIA", relógio 03:12, velocímetro 100/300 KM/H, "0,014 s", régua "3 MM / 2 CM", "363x / 900x O SEU PESO", etiquetas "• LUZ ACESA", "• ÚNICA SAÍDA", "• PISÃO", "• COAGULOU", setas vermelhas/laranjas.
- Humano aparece de corpo inteiro e com reação (susto, mão na cabeça); humano correndo na rua com velocímetro pra comparar velocidade.
- Mostra o mecanismo: pelos do cerco em macro com linhas de vento, corpo achatando com placas coloridas, corte do corpo por dentro, multidão de baratas empilhadas pra mostrar peso.
- A barata sempre se desloca de verdade no quadro (migalhas e chão passando).
Erros da nossa v1 (apontados pelo Thiago): chinelo/cavalo mal enquadrado; barata "patinando" (patas rápidas, corpo parado); virada na pia lenta demais; ralo: ela não sobe, fica esticada por cima; planos repetidos; não teve o humano correndo ao lado; voz robótica e lenta.
Regra para a v2: no mínimo 30 planos, 1 infográfico por plano, humano de corpo inteiro em 4+ planos, comparação de velocidade com o cavalo correndo, voz mais natural e ~10% mais rápida.

## PADRÃO APROVADO (barata v2, 10/11/2026) — Thiago: "quero que os outros vídeos sejam igual a esse ou melhor"
- Referência: barata3d/v2 (cena2.py = head.py + shots_def.py + tail.py, compor.py).
- Uma cena por frase (41 cortes em 83 s), texto/infográfico em quase toda cena, legenda palavra a palavra.
- Voz Antonio conversada (rate/pitch por frase), sem cara de leitura.
- Fluxo: teste de voz → storyboard com todas as cenas pra aprovação → render no GitHub (20 partes, ~1h30) → montagem.
- Interpolação LINEAR dentro da cena (câmera acompanha o bicho), câmera nunca dentro de móveis.
