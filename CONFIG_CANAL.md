# Configuração do canal Nunca Visto

Não coloque senhas aqui.

## QUALIDADE (desde 04/11/2026 — meta: sair dos 300-1.000 views)
- VOZ: o tts_lines.py agora usa uma voz neural natural (sozinho). Não mude.
- EFEITOS: o render.py já coloca um "whoosh" em toda troca de cena. No spec.json marque "impacto": true na cena do FATO MAIS SURPREENDENTE (só 1) e, quando combinar, "efeito": explosao | trovao | agua | vento | coracao | grave | brilho na cena certa.
- RITMO DA IMAGEM rápido (cena longa vira 2 tomadas sozinha), mas a FALA calma e clara: no máximo 2,8 palavras por segundo no vídeo inteiro (o qc.py confere). Nunca encurte frase cortando palavra.
- EXPLICAR SEM PULAR ETAPA (pedido do Thiago): cada frase leva à próxima, na ordem: o que é -> onde/quando -> por que acontece -> o número que impressiona -> o que isso significa. Se o espectador precisar saber algo para entender a próxima frase, essa informação TEM que vir antes. Termos difíceis: explique em 4 ou 5 palavras simples. Pode durar até 50 segundos se precisar para explicar direito.
- REVISÃO AUTOMÁTICA OBRIGATÓRIA: depois do render rode "python3 qc.py spec.json out". Só publique se sair APROVADO. Se sair REPROVADO, corrija o que ele listar e renderize de novo (até 3 vezes). O Thiago NÃO revisa os vídeos antes de ir ao ar: o robô é o único filtro.
- Antes de publicar, leia o roteiro como alguém de 14 anos que nunca ouviu falar do assunto: entendeu tudo de primeira? Se não, reescreva.
- FINAL: última cena com pergunta que DIVIDE opinião ("Você entraria nesse lago?", "Você teria coragem?") — comentário empurra o vídeo. Quando der, a última frase emenda no gancho (faz assistir de novo).
- 1º SEGUNDO: a imagem mais impressionante + a frase mais forte. Se a pessoa precisar de 3 segundos para entender o que é, ela já pulou.

## ESPAÇO (atualizado em 03/11/2026)
A semana só de espaço foi testada e as views caíram (de ~1.000 para 100-350). Voltou o rodízio normal de categorias.
- Espaço entra no máximo 1 a cada 4 vídeos, e só assunto de PERIGO ou ABSURDO (buraco negro engolindo estrela, asteroide perto da Terra, estrela em velocidade absurda) — os únicos de espaço que passaram de 800 views.
- Nunca 2 vídeos de espaço seguidos.

## SUGESTÕES DE VÍDEO
- [x] PEDIDO DO THIAGO (fazer no PRÓXIMO vídeo, vale mais que o rodízio e a regra de espaço): COMPARAÇÃO DO TAMANHO DOS PLANETAS DO SISTEMA SOLAR. Gancho: muita gente acha que a Terra é um dos maiores planetas, mas 4 planetas são MUITO maiores (Júpiter, Saturno, Urano, Netuno). Mostre em ordem crescente: Mercúrio, Marte, Vênus, Terra (a maior das rochosas), Netuno, Urano, Saturno, Júpiter. NÃO inclua o Sol (o Thiago pediu: todo mundo já sabe que ele é o maior); o vídeo termina em Júpiter, o maior planeta. Use números simples e confirmados na NASA (ex.: quantas Terras cabem lado a lado no diâmetro de Júpiter; quantas Terras cabem dentro dele). Use imagens/vídeos REAIS da NASA de cada planeta e, se achar, a ilustração oficial da NASA de comparação de tamanhos (selo IMAGEM ILUSTRATIVA). Pode durar ATÉ 75 SEGUNDOS para explicar tudo direito (só neste vídeo, a regra de 28-40s não vale).
  IMAGENS DE COMPARAÇÃO (pedido do Thiago): monte você mesmo com Python/PIL imagens 1080x1920 em fundo preto com os planetas LADO A LADO, um do lado do outro, no TAMANHO PROPORCIONAL REAL entre eles, usando fotos REAIS da NASA de cada planeta (as fotos de disco inteiro em fundo preto: recorte o círculo). Embaixo de cada planeta escreva o NOME e o DIÂMETRO em km (ex.: "TERRA • 12.742 km", "JÚPITER • 139.820 km", números da NASA). Faça uma imagem por cena, acumulando: cena da Terra mostra Mercúrio, Marte, Vênus e Terra; a de Netuno acrescenta Netuno ao lado, e assim por diante — quando um planeta grande entra, os pequenos ficam minúsculos (esse é o choque). Use "fit": true nessas cenas e selo "TAMANHO REAL" (não IMAGEM ILUSTRATIVA). Alterne com 1 ou 2 vídeos reais da NASA (Júpiter da Juno, Saturno da Cassini) para ter movimento. (03/11/2026)
- [x] Sugestão de vídeo para hoje: BURACO NEGRO engolindo uma estrela (evento de ruptura por maré). Gancho de medo no 1º segundo. Use vídeo/simulação de alta qualidade da NASA SVS ou ESO com selo "IMAGEM ILUSTRATIVA". (01/11/2026)
- [x] Sugestão de vídeo para hoje: células HeLa, as células humanas "imortais". Em 1951, tiraram células do tumor de Henrietta Lacks sem ela saber. Ela morreu meses depois, mas as células dela continuam se multiplicando em laboratórios até hoje e ajudaram a criar a vacina da pólio. Gancho: "Essa mulher mo (21/10/2026)

## O QUE PROCURAR
- Gancho com NÚMERO FORTE ou RECORDE/EXTREMO logo na primeira frase (ex.: "vive mais de 250 anos", "o mais fundo", "o único que..."). Esse formato deu mais views (tubarão-da-groenlândia, ~1.700).
- Isso vale para mais ou menos METADE dos vídeos. A outra metade continua livre para assuntos interessantes e pouco falados, que quase ninguém conhece (como HeLa), mesmo sem recorde. Prefira o raro e surpreendente ao óbvio.
- Varie o tipo de assunto entre os vídeos seguidos (animal, oceano, espaço, Terra, corpo humano, história da ciência). Não repita o tema principal de nenhum dos últimos 10 vídeos.

## HISTÓRICO DE ASSUNTOS (já feitos, NUNCA repetir o assunto, mesmo com outro título ou imagem)
O feed público mostra só os últimos 15 vídeos, então vídeos mais antigos são esquecidos. Esta lista é a memória completa: confira ela E o feed antes de escolher. Depois de publicar, acrescente aqui uma linha com o assunto do vídeo novo (e commite junto).
- delta do Atchafalaya (terra nova na Louisiana)
- cachoeira submarina do Estreito da Dinamarca
- sombra da Lua vista do espaço (eclipse 2017)
- fumaça de incêndios do Canadá cruzando o Atlântico
- astronauta que cresce até 5 cm no espaço
- ganso-de-cabeça-listrada voando sobre o Himalaia
- submarino à deriva 31 dias em 1969
- lagos do Alasca que soltam metano que pega fogo
- helicóptero Ingenuity em Marte (72 voos)
- Mar de Aral que sumiu
- células HeLa / Henrietta Lacks
- ilha-vulcão que explodiu (fumaça a 58 km)
- tempestade de poeira cobrindo um quarto de Marte
- gelo que some e elevaria o mar 170 m
- montanha que perdeu 400 m num dia
- Sol cuspindo nuvem (ejeção de massa coronal)
- rachadura de 110 km na Antártida
- tubarão-da-groenlândia (mais de 250 anos)
- polvo de águas profundas que guardou os ovos por 53 meses (Graneledone boreopacifica)
- ossos do astronauta e exercício no espaço (esteira com cordas)
- Anomalia do Atlântico Sul (ponto fraco do campo magnético sobre o Brasil)
- sonda DART da NASA que bateu no asteroide Dimorfos (órbita 33 min mais rápida)
- lula-de-nadeira-grande (Magnapinna, braços 20x o corpo)
- sifonóforo gigante de 46 m (animal mais comprido já registrado, Ningaloo 2020)
- migração de zebras Okavango–Makgadikgadi (cercas 1968-2004)
- rio Colorado que parou de chegar ao mar e recebeu água de propósito (2014)
- Voyager 1 a 1 dia-luz da Terra (conserto da memória em 2024)
- maior esponja já encontrada (esponja-de-vidro do tamanho de uma van, Havaí 2015)
- Duobrachium sparksae: ctenóforo descrito só por vídeo (NOAA, 2015)
- anéis de Saturno sumindo (chuva de anel, NASA 2018)
- coral-negro que vive mais de 4 mil anos (Leiopathes, NOAA)
- quíton predador (Placiphorella, NOAA Papahānaumokuākea 2025)
- buraco negro que rasgou uma estrela (evento de ruptura por maré ASASSN-19bt, TESS)
- Grande Mancha Vermelha de Júpiter (tempestade com mais de 100 anos, encolhendo e ficando mais alta)
- tempestade solar de 1859 (Carrington) e a de 2012 que errou a Terra
- pepino-do-mar que nada (monstro galinha sem cabeça, Enypniastes, NOAA)
- Grande Lago Salgado de Utah encolhendo (NASA SVS, recorde de baixa 2022)

## VÍDEOS LONGOS (divulgar nos Shorts do mesmo tema)
Se o assunto do Short for do mesmo tema de um vídeo longo abaixo, a PRIMEIRA linha da descrição tem que ser:
"🎥 Vídeo completo: <título do longo> → <link>"
- Tema: oceano / fundo do mar / criaturas marinhas → "Filmaram isso no fundo do mar: 10 coisas que você nunca viu" → https://youtu.be/IMSlcE8tl_8
- Tema: animais que vivem muito / idade / longevidade → "Esse tubarão pode ter 400 anos (e não é o mais velho)" → https://youtu.be/WK_EoSqI-XM

## EVITAR
- OBRIGATÓRIO: antes de escolher o tema, leia o arquivo HISTORICO.md (lista COMPLETA de todos os vídeos já feitos; o feed do YouTube só mostra os últimos 15). Proibido repetir qualquer assunto ou bicho de lá (ex.: o sifonóforo gigante saiu 2 vezes: 15/10 e 28/10).
- Assuntos banais, que a pessoa já viu na escola ou no Google
- Lendas, teorias sem prova e exageros
- Repetir o mesmo ASSUNTO com outro ângulo (ex.: 'astronauta cresce no espaço' e depois 'astronauta perde osso no espaço' = repetido). Corpo do astronauta no espaço: ESGOTADO.
- Final bagunçado: as 2 últimas cenas precisam de imagem clara e inteira (nada de tela quase preta, imagem cortada no canto, quadro todo vermelho/branco de sinal perdido, ou legenda em inglês queimada embaixo). Se não tiver imagem boa pro final, termine na imagem mais forte do vídeo.
- Números mal explicados (ex.: '33 minutos mais rápido' em vez de 'a volta ficou 33 minutos mais curta'): fale do jeito que uma pessoa leiga entende na hora.
- Mesmo personagem/lugar/bicho de um vídeo dos últimos 15 dias (astronauta, polvo, Marte, Lua...)
- Terminar SEMPRE sem chamada: em mais ou menos metade dos vídeos (alternando), a última cena narra a pergunta e logo depois "Segue o canal pra ver o que você nunca viu."

## PAUSAS
