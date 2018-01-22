var style = document.createElement("style");
document.head.appendChild(style);
sheet = style.sheet;
sheet.addRule('h1:before', 'background-image: url(/non-static' + window.location.pathname + '/icon.png)');

function rightSidebarCalculations() {
    if (window.innerWidth >= 1295 && enable_right_sidebar && window.innerWidth < 1795) {
        // 280 nav, min 700 content, 300 right nav + 15 margin
        if (document.getElementsByClassName('article_content').length === 1) {
            var new_width = window.innerWidth - 595;
            document.getElementsByClassName('article_content')[0].style.width = new_width + 'px';
            document.getElementById('right_sidebar').style.display = 'flex';
            document.getElementById('right_sidebar').style.marginLeft = (window.innerWidth - 315) + 'px';
        }
    } else if (window.innerWidth > 1795) {
        // 280 nav, max 1200 content, 300 right nav + 15 margin
        if (document.getElementsByClassName('article_content').length === 1) {
            document.getElementsByClassName('article_content')[0].style.width = '1200px';
            document.getElementById('right_sidebar').style.display = 'flex';
            document.getElementById('right_sidebar').style.marginLeft = '1480px';
        }
    } else {
        document.getElementsByClassName('article_content')[0].style.maxWidth = '1200px';
        document.getElementsByClassName('article_content')[0].style.width = '';
        document.getElementById('right_sidebar').style.display = 'none';
    }
}

window.addEventListener('load', function() {
    rightSidebarCalculations();
}, true);

window.addEventListener('resize', function(){
  rightSidebarCalculations();
});
