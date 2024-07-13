document.addEventListener('DOMContentLoaded', function () {
  const monkeyIcon = document.querySelector('h1 span.monkey-icon');
  const searchInput = document.querySelector('#search-input');
  let animationTriggered = false;

  function startConfetti() {
    const body = document.body;
    const fireworksContainer = document.createElement('div');
    fireworksContainer.id = 'fireworks-container';
    body.appendChild(fireworksContainer);

    for (let i = 0; i < 100; i++) {
      createConfetti(fireworksContainer);
      createStreamer(fireworksContainer);
    }

    setTimeout(() => {
      body.removeChild(fireworksContainer);
    }, 6400);
  }

  function createConfetti(container) {
    const confetti = document.createElement('div');
    confetti.classList.add('confetti');
    container.appendChild(confetti);

    confetti.style.setProperty('--confetti-color', getRandomColor());
    confetti.style.setProperty('--confetti-angle', `${Math.random() * 360}deg`);

    confetti.style.top = `${Math.random() * 100}%`;
    confetti.style.left = `${Math.random() * 100}%`;

    confetti.style.animationDuration = `${Math.random() * 8 + 1}s`;
    confetti.style.animationDelay = `${Math.random() * 2}s`;

    confetti.addEventListener('animationend', () => {
      container.removeChild(confetti);
    });
  }

  function createStreamer(container) {
    const streamer = document.createElement('div');
    streamer.classList.add('streamer');
    container.appendChild(streamer);

    streamer.style.top = `${Math.random() * 100}%`;
    streamer.style.left = `${Math.random() * 100}%`;

    streamer.style.animationDuration = `${Math.random() * 8 + 1}s`;
    streamer.style.animationDelay = `${Math.random() * 2}s`;

    streamer.addEventListener('animationend', () => {
      container.removeChild(streamer);
    });
  }

  function getRandomColor() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  function explodeMonkey(monkeyIcon) {
    setTimeout(() => {
      startConfetti(); // Burst confetti

      // Create multiple pieces for the explosion effect
      for (let i = 0; i < 50; i++) {
        createConfettiPiece(monkeyIcon);
      }

      // Hide the monkey icon
      monkeyIcon.style.opacity = '0';
    }, 1000);
  }

  function createConfettiPiece(monkeyIcon) {
    const piece = document.createElement('div');
    piece.classList.add('monkey-piece');
    document.body.appendChild(piece);

    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
    const shapes = ['circle', 'square', 'triangle'];

    // Random color
    piece.style.setProperty('--color', colors[Math.floor(Math.random() * colors.length)]);

    // Random shape
    const shape = shapes[Math.floor(Math.random() * shapes.length)];
    switch (shape) {
      case 'circle':
        piece.style.width = '20px';
        piece.style.height = '20px';
        piece.style.borderRadius = '50%';
        piece.style.backgroundColor = piece.style.getPropertyValue('--color');
        break;
      case 'square':
        piece.style.width = '20px';
        piece.style.height = '20px';
        piece.style.borderRadius = '0';
        piece.style.backgroundColor = piece.style.getPropertyValue('--color');
        break;
      case 'triangle':
        piece.style.width = '0';
        piece.style.height = '0';
        piece.style.borderLeft = '10px solid transparent';
        piece.style.borderRight = '10px solid transparent';
        piece.style.borderBottom = `20px solid ${piece.style.getPropertyValue('--color')}`;
        break;
    }

    // Random distance and angle for the explosion to cover the full viewport width
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    piece.style.setProperty('--distance', `${Math.random() * vw + vh}px`); // Covers full width and some height
    piece.style.setProperty('--angle', `${Math.random() * 2 * Math.PI}`);
    piece.style.setProperty('--rotation', `${Math.random() * 720 - 360}deg`);

    // Position the piece at the center of the monkey icon
    piece.style.position = 'absolute';
    piece.style.top = `${monkeyIcon.offsetTop + monkeyIcon.offsetHeight / 2}px`;
    piece.style.left = `${monkeyIcon.offsetLeft + monkeyIcon.offsetWidth / 2}px`;

    // Add animation
    piece.style.animation = 'explode-animation 1s ease-out forwards';

    piece.addEventListener('animationend', () => {
      document.body.removeChild(piece);
    });
  }

  function moveToCenterAndExplode() {
    const vw = window.innerWidth;
    const vh = window.innerHeight;

    // Save initial position
    monkeyIcon.style.setProperty('--initial-top', `${monkeyIcon.offsetTop}px`);
    monkeyIcon.style.setProperty('--initial-left', `${monkeyIcon.offsetLeft}px`);

    // Trigger the move-to-center animation
    setTimeout(() => {
      monkeyIcon.classList.add('move-to-center');
    }, 800);

    monkeyIcon.addEventListener('animationend', () => {
      explodeMonkey(monkeyIcon);
    }, { once: true });
  }

  function triggerZippy() {
    if (!animationTriggered) {
      const vw = window.innerWidth;
      const vh = window.innerHeight;

      // Set constrained random positions for the zippy animation with bias
      monkeyIcon.style.setProperty('--x1', `${Math.random() * 0.75 - 0.375}`);
      monkeyIcon.style.setProperty('--y1', `${Math.random() * 0.75 - 0.125}`);
      monkeyIcon.style.setProperty('--x2', `${Math.random() * 0.75 - 0.375}`);
      monkeyIcon.style.setProperty('--y2', `${Math.random() * 0.75 - 0.125}`);
      monkeyIcon.style.setProperty('--x3', `${Math.random() * 0.75 - 0.375}`);
      monkeyIcon.style.setProperty('--y3', `${Math.random() * 0.75 - 0.125}`);
      monkeyIcon.style.setProperty('--x4', `${Math.random() * 0.75 - 0.375}`);
      monkeyIcon.style.setProperty('--y4', `${Math.random() * 0.75 - 0.125}`);
      monkeyIcon.style.setProperty('--x5', `${Math.random() * 0.75 - 0.375}`);
      monkeyIcon.style.setProperty('--y5', `${Math.random() * 0.75 - 0.125}`);

      // Set random rotation degrees for each keyframe
      monkeyIcon.style.setProperty('--r1', `${Math.random() * 360}deg`);
      monkeyIcon.style.setProperty('--r2', `${Math.random() * 360}deg`);
      monkeyIcon.style.setProperty('--r3', `${Math.random() * 360}deg`);
      monkeyIcon.style.setProperty('--r4', `${Math.random() * 360}deg`);
      monkeyIcon.style.setProperty('--r5', `${Math.random() * 360}deg`);

      monkeyIcon.classList.add('zippy');
      startConfetti();

      setTimeout(() => {
        monkeyIcon.classList.remove('zippy');
        monkeyIcon.classList.add('zippy-reverse');
      }, 3250);

      setTimeout(() => {
        monkeyIcon.classList.remove('zippy-reverse');
        moveToCenterAndExplode();
      }, 6450);

      animationTriggered = true;
    }
  }

  function shouldTriggerZippy() {
    return Math.random() < 0.1; // chance for ZippyMonkey
  }
  function shouldTriggerBouncy() {
    return Math.random() < 0.1; // chance for BouncyMonkey
  }

  function triggerBouncy() {
    // Initial fall out
    monkeyIcon.classList.add('fall');

    // Wait for the initial fall-out animation to complete
    setTimeout(() => {
      // Switch to fixed position and start bouncing
      monkeyIcon.classList.remove('fall');
      monkeyIcon.classList.add('bouncy-ball');
    }, 1000); // Duration of the fall-out animation

    setTimeout(() => {
      monkeyIcon.classList.remove('bouncy-ball');
      moveToCenterAndExplode();
    }, 6600);
  }

  function startJigglyAnimation() {
    if (!animationTriggered) {
      monkeyIcon.classList.add('jiggly-monkey');
    }
  }

  function stopJigglyAnimation() {
    monkeyIcon.classList.remove('jiggly-monkey');
    animationTriggered = true;
  }

  function getRandomInterval(min, max) {
    return Math.random() * (max - min) + min;
  }

  function setJigglyAnimation() {
    if (!animationTriggered) {
      startJigglyAnimation();
      setTimeout(stopJigglyAnimation, 1600); // Adjust the timeout to match the animation duration
      setTimeout(setJigglyAnimation, getRandomInterval(1800, 5000)); // Schedule next jiggly animation
    }
  }

  if (monkeyIcon) {
    setTimeout(setJigglyAnimation, getRandomInterval(1800, 5000)); // Start the first jiggly animation

    monkeyIcon.addEventListener('mouseenter', () => {
      animationTriggered = true;
      stopJigglyAnimation(); // Stop the jiggly animation on hover

      if (shouldTriggerZippy()) {
        triggerZippy();
      } else if (shouldTriggerBouncy()) {
        triggerBouncy();
      } else {
        monkeyIcon.classList.add('spiral');
        setTimeout(() => {
          monkeyIcon.classList.remove('spiral');
          monkeyIcon.style.transform = 'rotate(180deg)'; // Ensure the monkey is upside down
        }, 20000);
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const searchText = searchInput.value.toLowerCase();
      if (searchText === 'dance monkey') {
        stopJigglyAnimation();
        triggerZippy();
      } else if (searchText === 'jump monkey') {
        stopJigglyAnimation();
        triggerBouncy();
      }
    });
  }
});
