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
- (08/11/2026, o Thiago reclamou: "só vejo espaço") Conta como ESPAÇO tudo que tem Lua, planeta, NASA no título, satélite, astronauta ou "visto do espaço". O robô estava escolhendo tema pelo banco de imagens da NASA e caindo em espaço quase todo dia. PROIBIDO espaço nos próximos 5 vídeos. Prioridade agora: TERRA e ANIMAIS (vulcão, raio, tempestade, caverna, deserto, bicho com comportamento absurdo, corpo humano). Imagem de bicho/natureza pode vir do Wikimedia Commons, Pexels ou Pixabay — não precisa ser NASA. Não use "NASA" no título.
- RODÍZIO FIXO (depois da pausa): olhe a categoria do ÚLTIMO vídeo no HISTORICO.md e faça a próxima desta ordem: TERRA (vulcão, raio, caverna, deserto, fenômeno) → ANIMAL → CORPO HUMANO → OCEANO → ANIMAL → ESPAÇO (perigo/absurdo) → volta pra TERRA.

## SUGESTÕES DE VÍDEO
- [ ] Crie um vídeo hiper-realista inspirado na gameplay de GTA 6. A câmera está no banco de trás de um carro, com uma pessoa gravando pelo celular a movimentação das ruas de Vice City. Trânsito, carros esportivos, pedestres e iluminação natural de Miami. Estilo cinematográfico, câmera de celular na mão, (12/11/2026)
- [x] PEDIDO DO THIAGO (fazer no PRÓXIMO vídeo, vale mais que o rodízio e a regra de espaço): COMPARAÇÃO DO TAMANHO DOS PLANETAS DO SISTEMA SOLAR. Gancho: muita gente acha que a Terra é um dos maiores planetas, mas 4 planetas são MUITO maiores (Júpiter, Saturno, Urano, Netuno). Mostre em ordem crescente: Mercúrio, Marte, Vênus, Terra (a maior das rochosas), Netuno, Urano, Saturno, Júpiter. NÃO inclua o Sol (o Thiago pediu: todo mundo já sabe que ele é o maior); o vídeo termina em Júpiter, o maior planeta. Use números simples e confirmados na NASA (ex.: quantas Terras cabem lado a lado no diâmetro de Júpiter; quantas Terras cabem dentro dele). Use imagens/vídeos REAIS da NASA de cada planeta e, se achar, a ilustração oficial da NASA de comparação de tamanhos (selo IMAGEM ILUSTRATIVA). Pode durar ATÉ 75 SEGUNDOS para explicar tudo direito (só neste vídeo, a regra de 28-40s não vale).
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
- raios que sobem de tempestades: sprites, jatos azuis e fantasmas verdes vistos da ISS (NASA ScienceCast, 2026-11-05)
- rio Klamath: 4 represas derrubadas (maior remoção do mundo), salmões voltando (NASA SVS 15027, 2026-11-05)
- peixe que anda no fundo do mar (armored searobin, NOAA; tamboril de Schaefer também "caminha", 2026-11-05)
- lulas Illex que se atacam e lagosta comendo os pedaços (squid storm, NOAA Deep Connections 2019, 2026-11-06)
- pinguim-imperador que mergulha mais de 500 m e baixa o coração a ~6 batidas/min (Jessica Meir, NASA JSC, 2026-11-06)
- tsunami de Kamchatka detectado pelo céu (GUARDIAN, NASA SVS 5625; SWOT, 2026-11-06)
- lulas-do-Havaí bebês na ISS, experimento UMAMI (NASA, CRS-22, 2026-11-07)
- formigas-de-correição que fazem ponte viva com o corpo (Eciton burchellii, Garnier et al. 2013 PLOS, 2026-11-12)

## VÍDEOS LONGOS (divulgar nos Shorts do mesmo tema)
Se o assunto do Short for do mesmo tema de um vídeo longo abaixo, a PRIMEIRA linha da descrição tem que ser:
"🎥 Vídeo completo: <título do longo> → <link>"
- Tema: oceano / fundo do mar / criaturas marinhas → "Filmaram isso no fundo do mar: 10 coisas que você nunca viu" → https://youtu.be/IMSlcE8tl_8
- Tema: animais que vivem muito / idade / longevidade → "Esse tubarão pode ter 400 anos (e não é o mais velho)" → https://youtu.be/WK_EoSqI-XM

## EVITAR
- (12/11/2026, o Thiago reclamou de NOVO) Três vídeos seguidos de ÁGUA/MAR ("água a 350 graus", "tartarugas travadas de frio", "vulcão com mangueira de lava no mar") = repetitivo e quase sem views (6 a 68). PROIBIDO por 30 dias: mar, oceano, água, vulcão submarino, lava no mar, fonte termal, tartaruga marinha.
- (12/11/2026) FILTRO "INÉDITO" OBRIGATÓRIO: só passa animal ou fenômeno que uma pessoa comum NUNCA viu e NUNCA ouviu falar. Prefira: espécies descobertas nos últimos anos, bicho bizarro FILMADO fazendo algo que parece mentira, fenômeno raro registrado em vídeo. Se o assunto é conhecido (já virou meme, aparece em todo canal de curiosidade, é matéria de escola), DESCARTE e escolha outro.
- (12/11/2026) FINAL SEM PERGUNTA BESTA: PROIBIDO terminar com "Você sabia?", "O que você acha?", "Você teria coragem?", "Comenta aí" ou qualquer pergunta. Vale MAIS que a regra do prompt sobre a última cena: a última cena (cta:true) narra o fato MAIS chocante/a virada do vídeo, em frase curta e forte. Pode, no máximo, completar com "Segue o canal pra ver o que você nunca viu." Na descrição do YouTube também não ponha pergunta.
- (12/11/2026, o Thiago reclamou: "só espaço e mar, nada da Terra") NOVO RODÍZIO, vale MAIS que o rodízio do prompt: Animais -> Terra -> Corpo Humano -> Animais -> Terra -> Oceano/Espaço (um OU outro) -> repete. ESPAÇO no máximo 1 vídeo a cada 6 e OCEANO no máximo 1 a cada 6. Motivo (views): bicho e Terra deram ~1.000 (pinguim 966, cratera sob o gelo 1.053, lulas 1.007, mosca/barata/pernilongo 900-1.100); espaço deu 86-215.
  * TERRA = coisas do planeta que a pessoa nunca viu: fenômenos (raio vulcânico, nuvem estranha, deserto que floresce, cristais gigantes, cavernas, terremoto filmado, areia que canta), lugares absurdos. ANIMAIS = bicho com comportamento que parece mentira, de preferência que o brasileiro conhece (tatu, capivara, formiga, urubu, sapo, tamanduá) ou bicho bizarro filmado.
- (07/11/2026) LULA PROIBIDA por 30 dias (saíram 3 de lula em 3 semanas e "lulas bebês no espaço" foi REPETIDO: 20/10 e 07/11). ANTES de escolher o tema, leia o HISTORICO.md INTEIRO e procure o animal/assunto pelo nome: se já saiu, é PROIBIDO, mesmo com outro título.
- (05/11/2026, o Thiago achou repetitivo e ruim) PROIBIDO por 30 dias o tipo "algo está SUMINDO / SECANDO / RECUANDO / DERRETENDO" (geleira, lago, rio, gelo, mudança do clima). Foram 4 seguidos. Volte ao que dava ~1.000 views: "parece mentira mas é real" com imagem impressionante — animal com comportamento absurdo, criatura do fundo do mar, fenômeno raro filmado (raio, explosão, vulcão), corpo humano surpreendente.
- UM VÍDEO POR EXECUÇÃO: antes do push, confira que a pasta publicar/ tem EXATAMENTE 1 .mp4 e 1 .json (em 04/11 foram 2 vídeos iguais de uma vez). Se tiver sobra de execução anterior, apague antes do commit.
- O histórico de assuntos é o HISTORICO.md (não só o feed do YouTube): vídeo que sumiu do feed foi APAGADO pelo Thiago, não está liberado para refazer.
- (05/11/2026, o Thiago apagou um vídeo por isso) PROIBIDO por 30 dias qualquer assunto de RIO, LAGO, REPRESA, DELTA ou ÁGUA DOCE: o canal fez 5 vídeos de rio/lago em 3 semanas e ficou repetitivo. Assunto já publicado sobre rio (Klamath/represas, Louisiana, rio que voltou ao mar, rio dentro do oceano, Grande Lago Salgado) NUNCA mais.
- FAMÍLIA DE ASSUNTO: antes de escolher, veja os últimos 15 títulos do HISTORICO.md e agrupe por família (ex.: rio/lago/represa = mesma família; vulcão/terremoto; buraco negro/estrela; tubarão/peixe). Se a família do seu tema aparece 2 vezes ou mais nos últimos 15, escolha outra família.
- Se o Thiago apagou um vídeo, o assunto dele está proibido para sempre (não refaça o mesmo vídeo).
- OBRIGATÓRIO: antes de escolher o tema, leia o arquivo HISTORICO.md (lista COMPLETA de todos os vídeos já feitos; o feed do YouTube só mostra os últimos 15). Proibido repetir qualquer assunto ou bicho de lá (ex.: o sifonóforo gigante saiu 2 vezes: 15/10 e 28/10).
- Assuntos banais, que a pessoa já viu na escola ou no Google
- Lendas, teorias sem prova e exageros
- Repetir o mesmo ASSUNTO com outro ângulo (ex.: 'astronauta cresce no espaço' e depois 'astronauta perde osso no espaço' = repetido). Corpo do astronauta no espaço: ESGOTADO.
- Final bagunçado: as 2 últimas cenas precisam de imagem clara e inteira (nada de tela quase preta, imagem cortada no canto, quadro todo vermelho/branco de sinal perdido, ou legenda em inglês queimada embaixo). Se não tiver imagem boa pro final, termine na imagem mais forte do vídeo.
- Números mal explicados (ex.: '33 minutos mais rápido' em vez de 'a volta ficou 33 minutos mais curta'): fale do jeito que uma pessoa leiga entende na hora.
- Mesmo personagem/lugar/bicho de um vídeo dos últimos 15 dias (astronauta, polvo, Marte, Lua...)

## PAUSAS
