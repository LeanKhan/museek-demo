$(document).ready(function () {
    $(window.location.hash).modal('show');
    $('a.open-modal-hash').click(function () {
        window.location.hash = $(this).attr('href');

        $(window.location.hash).modal('show');
    });

    $(".modal").on("hidden.bs.modal", function () { // any time a modal is hidden
        var urlReplace = window.location.toString().split('#', 1)[0];
        history.pushState(null, null, urlReplace); // push url without the hash as new history item
    });
});