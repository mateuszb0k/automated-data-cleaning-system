bg_css = """
<style>
@keyframes moveClouds {
    from { background-position: 0px 0px; }
    to { background-position: 10000px 0px; }
}
.stApp {
    background-color: #eb8787;
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/1/16/Appearance_of_sky_for_weather_forecast%2C_Dhaka%2C_Bangladesh.JPG");
    background-size: cover;
    animation: moveClouds 300s linear infinite;
}
.block-container {
    background-color: rgba(255, 255, 255, 0.55);
    border-radius: 15px;
}
</style>
"""