"use strict";

const qBtnYes = document.querySelector("#permission-yes");
const qBtnNo = document.querySelector("#permission-no");
const qCheckCollege = document.querySelector("#college");
const qCSRF = document.querySelector("#csrf_token");
const ONE_MINUTE = 1000 * 60;


/**
 * Redirect to the no page. This is used when the user
 * denies access to their location or the api has an error.
 */
function handleError() {
  window.sessionStorage.setItem("location-denied", "true");
  window.location = Flask.url_for("date.no");
}

/**
 * Handle a sucessful geolocation request.
 *
 * @param {Position} posi
 */
function handleLocation(posi) {
  // Collect the info we need into one handy object
  const details = {
    lng: posi.coords.longitude,
    lat: posi.coords.latitude,
    acc: posi.coords.accuracy,
    col: qCheckCollege.checked
  };

  // Send the info to the back-end and redirect the user
  // to the proper results page accordingly
  fetch(Flask.url_for("date.form"), {
    method: "POST",
    body: JSON.stringify(details),
    headers: {
      "X-CSRFToken": qCSRF.value,
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
  })
  .then(r => r.text())
  .then(url => window.location = url);
}

/**
 * Handle permission form response.
 *
 * @param {Object} e
 */
function handleFormSubmission(e) {
  e.target.blur();

  // We were not grated permission to access the user's location
  if (e.target.id === "permission-no") {
    handleError();

  // The user grants permission to their location
  } else {
    navigator.geolocation.getCurrentPosition(handleLocation, handleError, {
      enableHighAccuracy: false,
      maximumAge: ONE_MINUTE * 2,
      timeout: ONE_MINUTE
    });
  }
}

// The user clicked one of the buttons in the form
qBtnYes.addEventListener("click", handleFormSubmission, {passive: true});
qBtnNo.addEventListener("click", handleFormSubmission, {passive: true});
