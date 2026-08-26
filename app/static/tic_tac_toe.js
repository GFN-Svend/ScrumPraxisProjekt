(() => {
  "use strict";

  const cells = [...document.querySelectorAll("[data-cell]")];
  const status = document.querySelector("#game-status");
  const resetButton = document.querySelector("#game-reset");
  const gameBoard = document.querySelector(".tic-tac-toe-board");
  const minkaFigure = document.querySelector(".minka-opponent");
  const minkaImage = document.querySelector("#minka-emote");
  const minkaSpeech = document.querySelector("#minka-speech");

  if (cells.length !== 9 || !status || !resetButton || !gameBoard
      || !minkaFigure || !minkaImage || !minkaSpeech) return;

  const HUMAN = "X";
  const CAT = "O";
  const MAX_PAWNS = 3;
  const CAT_MISTAKE_CHANCE = 0.12;
  const winningLines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
  ];

  let board = Array(9).fill("");
  let moveHistory = { [HUMAN]: [], [CAT]: [] };
  let isPlayersTurn = true;
  let gameOver = false;
  let catTimer = null;
  let playerReminderTimer = null;
  let lastCatMoveWasMistake = false;
  let minkaTouchCount = 0;
  let lastSpeechText = "";

  const speeches = {
    ready: [
      "Minka ist bereit.",
      "Na los, zeig mir deine beste Pfote.",
      "Eine neue Runde? Dieses Mal gewinne ich schneller.",
      "Nya dann – Pfoten auf den Tisch!",
      "Ich bin schnurrbereit. Du auch?",
      "Das wird eine echte Katzastrophe für dich.",
    ],
    thinking: [
      "Hm … wo setze ich meine Pfote hin?",
      "Das Feld riecht verdächtig nach einer Falle.",
      "Warte ab, Zweibeiner. Ich habe einen Plan.",
      "Miau … diese Pfote verlangt Köpfchen.",
      "Du machst es mir ja fast interessant.",
      "Ich weiß genyau, was ich tue. Fast.",
      "Das muss ich erst einmal durchmauzenken.",
      "Ein katzastisch kluger Zug kommt sofort.",
      "Nya warte, meine Schnurrhaare rechnen noch.",
      "Pfotenyalarm! Hier stimmt etwas nicht.",
    ],
    refresh: [
      "Mrrr! Das war mein Plan!",
      "Du hast die Pfote gerettet? Frechheit!",
      "Das zählt doch nur wegen deiner Finger!",
      "Na schön. Die Pfote darf noch bleiben.",
      "Unverschämnyat! Die war schon fast weg.",
      "Nya toll, jetzt muss ich neu nachdenken.",
      "Pfoten-Recycling? Typisch Zweibeiner.",
      "Das ist doch gemauschelt!",
    ],
    reminder: [
      "Dein Zug. Ich passe genau auf.",
      "Bist du eingeschlafen, Zweibeiner?",
      "Minka wartet nicht den ganzen Tag.",
      "Na los. Eine Pfote wird doch wohl drin sein.",
      "Soll ich deinen Zug auch noch machen?",
      "Nya? Ist da noch jemand?",
      "Meine Schnurrhaare werden schon grau.",
      "Beeilung, sonst mache ich ein Nickerchen.",
      "Du denkst aber verdächtig ungenyau.",
      "Miau mal Butter bei die Fische!",
    ],
    catWin: [
      "Ha! Drei Pfoten – ich gewinne!",
      "Miau-ha-ha! Das war viel zu einfach.",
      "Der Sieg gehört selbstverständlich der Katze.",
      "Du hattest wirklich geglaubt, du gewinnst?",
      "Schnurrzüglich gespielt – von mir natürlich.",
      "Nya-ha-ha! Das Brett gehört jetzt mir.",
      "Katzastisch! Bitte einmal den Sieger-Napf.",
      "Genyau so gewinnt eine Profi-Pfote.",
    ],
    humanWin: [
      "Was?! Wie hast du das gemacht?",
      "Unmöglich. Ich verlange eine neue Runde!",
      "Das Brett war eindeutig gegen mich.",
      "Genieß den Sieg. Es bleibt dein einziger.",
      "Unmögnyalich! Prüft sofort das Brett.",
      "Meine Schnurrhaare haben mich abgelenkt.",
      "Nya schön. Ein Punkt für den Dosenöffner.",
      "Das war nur ein strategisches Nickerchen.",
    ],
    exploit: [
      "Du hast meinen kleinen Patzer gesehen?!",
      "Das … war natürlich genau so geplant.",
      "Pah! Diesen Fehler nutzt du schamlos aus.",
      "Vergiss sofort, dass du das gesehen hast.",
      "Das war kein Fehler, das war eine Miaußnahme!",
      "Du hast genyau den falschen Moment bemerkt.",
      "Nya gut, der Zug war etwas pfotenlahm.",
      "Meine Schnurrhaare hatten kurz Funkstille.",
    ],
    exploitWin: [
      "Du gewinnst wegen dieses einen Patzers? Unverschämt!",
      "Nein! Mein Fehler war doch nur ein Test!",
      "Das zählt nicht. Meine Pfote ist ausgerutscht!",
      "Katzastrophe! Du hast meinen Patzer wirklich benutzt.",
      "Unmögnyalich – ein Zweibeiner hat aufgepasst!",
      "Nya toll. Ein Fehler, und du machst gleich drei Pfoten daraus.",
    ],
    touch: [
      "Ey, nicht anfassen!",
      "Nimm deine schmutzigen Finger aus meinem Fell!",
      "Ich habe dich gewarnt, Zweibeiner.",
      "Noch einmal und ich spiele mit Krallen!",
      "MRAU! Jetzt reicht es aber!",
      "Nya! Das ist Fell, kein Touchscreen!",
      "Pfoten weg von meiner Flauschzone!",
      "Unfassbar. Der Dosenöffner wird übermütig.",
      "Meine Schnurrhaare haben dich genyau im Blick.",
      "Streichelnyotstand! Sofort zurücktreten!",
      "Du provozierst eine ausgewachsene Katzastrophe.",
      "Ich bin Minka, nicht dein Staubwedel!",
    ],
    overpetted: [
      "PFOTENYALARM! Jetzt fliegt hier das Fell!",
      "Nya reicht's – aktiviere Krallenstufe Rot!",
      "Zu viel gestreichelt! Nimm das, Flauschdieb!",
      "Katzastrophe ausgelöst. Selbst schuld, Zweibeiner!",
    ],
  };

  function randomSpeech(pool) {
    const choices = pool.filter((speech) => speech !== lastSpeechText);
    const speech = choices[Math.floor(Math.random() * choices.length)] || pool[0];
    lastSpeechText = speech;
    return speech;
  }

  const minkaMoods = {
    neutral: { src: minkaImage.dataset.neutral, alt: "Minka wartet konzentriert hinter dem Spielfeld" },
    angry: { src: minkaImage.dataset.angry, alt: "Minka schaut wütend hinter dem Spielfeld hervor" },
    laughing: { src: minkaImage.dataset.laughing, alt: "Minka lacht schadenfroh über ihren Sieg" },
    defeated: { src: minkaImage.dataset.defeated, alt: "Minka reagiert überrascht auf ihre Niederlage" },
  };

  function setMinkaMood(mood, speech) {
    const nextMood = minkaMoods[mood];
    minkaFigure.dataset.mood = mood;
    minkaImage.src = nextMood.src;
    minkaImage.alt = nextMood.alt;
    minkaSpeech.textContent = speech || "";
    minkaSpeech.hidden = !speech;
  }

  function clearPlayerReminder() {
    if (playerReminderTimer !== null) window.clearTimeout(playerReminderTimer);
    playerReminderTimer = null;
  }

  function unleashFurStorm() {
    minkaFigure.classList.remove("is-overpetted");
    window.requestAnimationFrame(() => minkaFigure.classList.add("is-overpetted"));
    const stormSymbols = ["🐾", "✦", "〰", "🐾", "✧"];
    for (let index = 0; index < 12; index += 1) {
      const tuft = document.createElement("span");
      tuft.className = "fur-tuft";
      tuft.textContent = stormSymbols[index % stormSymbols.length];
      tuft.style.setProperty("--tuft-x", `${15 + Math.random() * 70}%`);
      tuft.style.setProperty("--tuft-delay", `${Math.random() * 180}ms`);
      tuft.style.setProperty("--tuft-drift", `${-55 + Math.random() * 110}px`);
      minkaFigure.append(tuft);
      tuft.addEventListener("animationend", () => tuft.remove(), { once: true });
      window.setTimeout(() => tuft.remove(), 1300);
    }
    window.setTimeout(() => minkaFigure.classList.remove("is-overpetted"), 900);
  }

  function winningLineFor(state, player) {
    return winningLines.find((line) => line.every((index) => state[index] === player));
  }

  function hasOpenThreat(state, player) {
    return winningLines.some((line) => (
      line.filter((index) => state[index] === player).length === 2
      && line.filter((index) => !state[index]).length === 1
    ));
  }

  function availableCellsIn(state) {
    return state.flatMap((value, index) => (value ? [] : [index]));
  }

  function availableActions(state, histories, player) {
    const actions = availableCellsIn(state).map((index) => ({ type: "place", index }));
    if (histories[player].length === MAX_PAWNS) {
      actions.push({ type: "refresh", index: histories[player][0] });
    }
    return actions;
  }

  function simulateAction(state, histories, action, player) {
    const nextBoard = [...state];
    const nextHistory = {
      [HUMAN]: [...histories[HUMAN]],
      [CAT]: [...histories[CAT]],
    };

    if (action.type === "refresh") {
      nextHistory[player].shift();
      nextHistory[player].push(action.index);
      return { board: nextBoard, history: nextHistory };
    }

    nextBoard[action.index] = player;
    nextHistory[player].push(action.index);
    if (nextHistory[player].length > MAX_PAWNS) {
      const expiredIndex = nextHistory[player].shift();
      nextBoard[expiredIndex] = "";
    }
    return { board: nextBoard, history: nextHistory };
  }

  function evaluatePosition(state) {
    if (winningLineFor(state, CAT)) return 10000;
    if (winningLineFor(state, HUMAN)) return -10000;
    const lineWeights = [0, 3, 22, 1000];
    let score = 0;
    winningLines.forEach((line) => {
      const cats = line.filter((index) => state[index] === CAT).length;
      const humans = line.filter((index) => state[index] === HUMAN).length;
      if (humans === 0) score += lineWeights[cats];
      if (cats === 0) score -= lineWeights[humans];
    });
    if (state[4] === CAT) score += 5;
    if (state[4] === HUMAN) score -= 5;
    return score;
  }

  function minimax(state, histories, player, depth, alpha, beta) {
    const positionScore = evaluatePosition(state);
    if (Math.abs(positionScore) >= 10000 || depth === 0) return positionScore;
    const actions = availableActions(state, histories, player);
    if (player === CAT) {
      let best = -Infinity;
      for (const action of actions) {
        const next = simulateAction(state, histories, action, CAT);
        best = Math.max(best, minimax(next.board, next.history, HUMAN, depth - 1, alpha, beta));
        alpha = Math.max(alpha, best);
        if (beta <= alpha) break;
      }
      return best;
    }
    let best = Infinity;
    for (const action of actions) {
      const next = simulateAction(state, histories, action, HUMAN);
      best = Math.min(best, minimax(next.board, next.history, CAT, depth - 1, alpha, beta));
      beta = Math.min(beta, best);
      if (beta <= alpha) break;
    }
    return best;
  }

  function chooseCatMove() {
    const rankedMoves = availableActions(board, moveHistory, CAT)
      .map((action) => {
        const next = simulateAction(board, moveHistory, action, CAT);
        return {
          action,
          score: minimax(next.board, next.history, HUMAN, 5, -Infinity, Infinity),
        };
      })
      .sort((left, right) => right.score - left.score);
    if (rankedMoves.length === 0) return undefined;
    lastCatMoveWasMistake = false;
    const weakerMoves = rankedMoves.filter((move) => move.score < rankedMoves[0].score);
    if (weakerMoves.length === 0 || Math.random() >= CAT_MISTAKE_CHANCE) {
      return rankedMoves[0].action;
    }
    const alternatives = weakerMoves.slice(0, Math.min(3, weakerMoves.length));
    lastCatMoveWasMistake = true;
    return alternatives[Math.floor(Math.random() * alternatives.length)].action;
  }

  function updateOldestPaws() {
    cells.forEach((cell) => cell.classList.remove("is-oldest", "is-refreshable"));
    for (const player of [HUMAN, CAT]) {
      if (moveHistory[player].length === MAX_PAWNS) {
        const oldestCell = cells[moveHistory[player][0]];
        oldestCell.classList.add("is-oldest");
        if (player === HUMAN) oldestCell.classList.add("is-refreshable");
      }
    }
    updateCellLabels();
  }

  function updateCellLabels() {
    cells.forEach((cell, index) => {
      if (!board[index]) {
        cell.setAttribute("aria-label", `Feld ${index + 1}, frei`);
      } else if (board[index] === HUMAN && cell.classList.contains("is-oldest")) {
        cell.setAttribute(
          "aria-label",
          `Feld ${index + 1}, deine älteste dunkle Pfote – zum Auffrischen anklicken`,
        );
      } else {
        cell.setAttribute(
          "aria-label",
          `Feld ${index + 1}, ${board[index] === HUMAN ? "deine dunkle Pfote" : "Minkas helle Pfote"}`,
        );
      }
    });
  }

  function clearCell(index) {
    board[index] = "";
    cells[index].replaceChildren();
    cells[index].className = "game-cell";
    cells[index].setAttribute("aria-label", `Feld ${index + 1}, frei`);
  }

  function placeMark(index, player) {
    board[index] = player;
    moveHistory[player].push(index);
    if (moveHistory[player].length > MAX_PAWNS) clearCell(moveHistory[player].shift());

    const paw = document.createElement("img");
    paw.className = "paw-token";
    paw.src = player === HUMAN ? gameBoard.dataset.darkPaw : gameBoard.dataset.lightPaw;
    paw.alt = "";
    paw.setAttribute("aria-hidden", "true");
    cells[index].replaceChildren(paw);
    cells[index].classList.add(player === HUMAN ? "is-human" : "is-cat");
    cells[index].setAttribute(
      "aria-label",
      `Feld ${index + 1}, ${player === HUMAN ? "deine dunkle Pfote" : "Minkas helle Pfote"}`,
    );
    cells[index].disabled = true;
    updateOldestPaws();
  }

  function refreshOldestPaw(player) {
    const refreshedIndex = moveHistory[player].shift();
    moveHistory[player].push(refreshedIndex);
    const paw = cells[refreshedIndex].querySelector(".paw-token");
    if (paw) {
      paw.classList.remove("is-refreshed");
      window.requestAnimationFrame(() => paw.classList.add("is-refreshed"));
    }
    updateOldestPaws();
  }

  function performAction(action, player) {
    if (action.type === "refresh") refreshOldestPaw(player);
    else placeMark(action.index, player);
  }

  function finishGame(player) {
    const line = winningLineFor(board, player);
    if (!line) return false;
    gameOver = true;
    clearPlayerReminder();
    line.forEach((index) => cells[index].classList.add("is-winning"));
    cells.forEach((cell) => { cell.disabled = true; });
    status.textContent = player === HUMAN
      ? "Gewonnen! Du hast Minka ausgetrickst."
      : "Minka gewinnt. Versuch es noch einmal!";
    setMinkaMood(
      player === HUMAN ? "defeated" : "laughing",
      player === HUMAN
        ? randomSpeech(lastCatMoveWasMistake ? speeches.exploitWin : speeches.humanWin)
        : randomSpeech(speeches.catWin),
    );
    return true;
  }

  function enableFreeCells() {
    const refreshableIndex = moveHistory[HUMAN].length === MAX_PAWNS
      ? moveHistory[HUMAN][0]
      : -1;
    cells.forEach((cell, index) => {
      cell.disabled = Boolean(board[index]) && index !== refreshableIndex;
    });
  }

  function catMove() {
    catTimer = null;
    if (gameOver) return;
    const action = chooseCatMove();
    if (action === undefined) return;
    performAction(action, CAT);
    if (!finishGame(CAT)) {
      isPlayersTurn = true;
      status.textContent = moveHistory[HUMAN].length === MAX_PAWNS
        ? "Du bist am Zug. Setze neu oder frische deine markierte Pfote auf."
        : "Du bist am Zug.";
      enableFreeCells();
      playerReminderTimer = window.setTimeout(() => {
        if (isPlayersTurn && !gameOver) {
          setMinkaMood("neutral", randomSpeech(speeches.reminder));
        }
      }, 10000);
      const nextCell = cells.find((cell, index) => !board[index]);
      if (nextCell) nextCell.focus();
    }
  }

  function handlePlayerMove(event) {
    const index = Number(event.currentTarget.dataset.cell);
    if (!isPlayersTurn || gameOver) return;
    clearPlayerReminder();

    const canRefresh = board[index] === HUMAN
      && moveHistory[HUMAN].length === MAX_PAWNS
      && moveHistory[HUMAN][0] === index;
    if (board[index] && !canRefresh) return;

    performAction(
      canRefresh ? { type: "refresh", index } : { type: "place", index },
      HUMAN,
    );
    if (finishGame(HUMAN)) return;
    const exploitedMistake = lastCatMoveWasMistake && hasOpenThreat(board, HUMAN);
    lastCatMoveWasMistake = false;
    isPlayersTurn = false;
    status.textContent = "Minka überlegt …";
    if (canRefresh) {
      setMinkaMood("angry", randomSpeech(speeches.refresh));
    } else if (exploitedMistake) {
      setMinkaMood("angry", randomSpeech(speeches.exploit));
    } else {
      setMinkaMood("neutral", randomSpeech(speeches.thinking));
      minkaFigure.dataset.mood = "thinking";
    }
    cells.forEach((cell) => { cell.disabled = true; });
    catTimer = window.setTimeout(catMove, 900);
  }

  function resetGame() {
    if (catTimer !== null) window.clearTimeout(catTimer);
    catTimer = null;
    clearPlayerReminder();
    board = Array(9).fill("");
    moveHistory = { [HUMAN]: [], [CAT]: [] };
    isPlayersTurn = true;
    gameOver = false;
    lastCatMoveWasMistake = false;
    status.textContent = "Du bist am Zug.";
    setMinkaMood("neutral", randomSpeech(speeches.ready));
    cells.forEach((cell, index) => {
      cell.replaceChildren();
      cell.disabled = false;
      cell.className = "game-cell";
      cell.setAttribute("aria-label", `Feld ${index + 1}, frei`);
    });
    cells[0].focus();
  }

  cells.forEach((cell) => cell.addEventListener("click", handlePlayerMove));
  resetButton.addEventListener("click", resetGame);
  minkaImage.addEventListener("click", () => {
    minkaTouchCount += 1;
    const isFurStorm = minkaTouchCount % 5 === 0;
    setMinkaMood(
      "angry",
      randomSpeech(isFurStorm ? speeches.overpetted : speeches.touch),
    );
    if (isFurStorm) unleashFurStorm();
  });
  minkaImage.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      minkaImage.click();
    }
  });
  Object.values(minkaMoods).forEach(({ src }) => {
    const preload = new Image();
    preload.src = src;
  });
})();
