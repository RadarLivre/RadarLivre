componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {
	var dialog = document.querySelector('dialog');
	var showDialogButton = document.querySelector('#rl-map__dialog-config');

	if(dialog != null && showDialogButton != null) {

		if (! dialog.showModal) {
			dialogPolyfill.registerDialog(dialog);
		}

		showDialogButton.addEventListener('click', function() {
			dialog.showModal();
		});

		dialog.querySelector('.rl-dialog__ok').addEventListener('click', function() {
			dialog.close();
		});
	}
});