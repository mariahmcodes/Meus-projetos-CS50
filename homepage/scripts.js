document.addEventListener('DOMContentLoaded', function() {
  // DARK MODE TOGGLE
  const toggleButton = document.querySelectorAll("#theme-toggle");
  toggleButton.forEach(btn => {
    btn.addEventListener('click', () => {
      document.body.classList.toggle("dark-mode");
    });
  });

  // PROJECT CARDS DYNAMIC CREATION
  const projectsContainer = document.getElementById("projects-container");
  if(projectsContainer){
    const projects = [
      {title: "CS50 PSET 1", description:"Solved basic programming problems using C and logic fundamentals.", link:"#"},
      {title: "CS50 PSET 2", description:"Worked with strings and cryptography, focusing on Caesar and Vigenère ciphers.", link:"#"},
      {title: "CS50 PSET 3", description:"Implemented a spell checker using hash tables to optimize dictionary lookups.", link:"#"},
      {title: "My First Flask App", description:"Built a simple web app using Flask and templates.", link:"#"}
    ];

    projects.forEach((project, i) => {
      const col = document.createElement("div");
      col.className = "col-sm-6 col-lg-4 mb-4";
      col.innerHTML = `
        <div class="card project-card h-100" style="animation-delay:${i*0.1}s">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">${project.title}</h5>
            <p class="card-text flex-grow-1">${project.description}</p>
            <a href="${project.link}" class="btn btn-outline-primary mt-auto" target="_blank">View Code/Demo</a>
          </div>
        </div>
      `;
      projectsContainer.appendChild(col);
    });
  }

  // CONTACT FORM FEEDBACK
  const submitBtn = document.querySelector('#submit-btn');
  if(submitBtn){
    submitBtn.addEventListener('click', function(e){
      e.preventDefault();
      const input = document.querySelector('#contact-input');
      const feedback = document.querySelector('#contact-feedback');
      if(input.value.trim() === ""){
        feedback.innerText = "Please type something!";
        feedback.style.color = "red";
      } else {
        feedback.innerText = "Message sent!";
        feedback.style.color = "green";
      }
    });
  }
});
