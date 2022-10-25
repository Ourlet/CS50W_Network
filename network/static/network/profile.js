document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#profile-view").style.display = "none";
  document.querySelector("#all-post").style.display = "block";
  document
    .querySelector("#followingButtons")
    .addEventListener("click", () => display_profile("Xavier"));
});

function display_profile(profile) {
  document.querySelector("#profile-view").style.display = "block";
  document.querySelector("#all-post").style.display = "none";

  // Call the API to get the details of the profile
  fetch(`/profile/${profile}`)
    .then((response) => response.json())
    .then((profile) => {
      // Create the container to show the email details
      console.log(profile);
      const element = document.createElement("div");

      // Add some HTML in the container to display the information of a specific email
      element.innerHTML = `<div class="user">
        <h2 id="profile">user : ${profile.username}</h2>
      </div>
    
      <div id="profile-details" class="profile">
        <ul>
          <li>Name: ${profile.firstname} ${profile.lastname}</li>
          <li>Account created : ${profile.accountCreated}</li>
    
          <li>Number of followers: ${profile.follower}</li>
          <li>Following: ${profile.followed}</li>
          <li>Is it currently following : ${profile.isFollowing}</li>
          <li>Is it own profile : ${profile.isOwnProfile}</li>
        </ul>
      </div>`;

      // Add the new HTML to the div email-details
      document.querySelector("#profile-view").append(element);
    });
}

function follow_profile(profile) {
  // Collect data from UI, user and profile viewed
  const profilViewed = document.querySelector(`${profile}`).innerHTML;
  console.log(profile);

  // Archive an email by changing status Archive = True
  fetch(`/profile/${profile}`, {
    method: "POST",
    body: JSON.stringify({
      profile: profilViewed,
    }),
  });
}
