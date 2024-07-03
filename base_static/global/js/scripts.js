(() => {
  const forms = document.querySelectorAll(".form-delete");

  for (const form of forms) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const confirmed = confirm("Are you sure?");

      if (confirmed) {
        form.submit();
      }
    });
  }
})();

(() => {
  const buttonCloseMenu = document.querySelector(".button-close-menu");
  const buttonShowMenu = document.querySelector(".button-show-menu");
  const menuContainer = document.querySelector(".menu-container");

  const buttonShowMenuVisibleClass = "button-show-menu-visible";
  const menuHiddenClass = "menu-hidden";

  const showMenu = () => {
    menuContainer.classList.remove(menuHiddenClass);
    buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
  };

  const closeMenu = () => {
    menuContainer.classList.add(menuHiddenClass);
    buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
  };

  if (buttonCloseMenu) {
    buttonCloseMenu.removeEventListener("click", closeMenu);
    buttonCloseMenu.addEventListener("click", closeMenu);
  }

  if (buttonShowMenu) {
    buttonShowMenu.removeEventListener("click", showMenu);
    buttonShowMenu.addEventListener("click", showMenu);
  }
})();
