const show_notify = (str, {type="normal", title="", timeout=5000, buttons=[], layout=1, color=false}={}) => {
	if(type === "normal"){
		iziToast.show({
			position: 'topRight',
			color: color ? color : 'blue',
			title: title,
			message: str,
			timeout: timeout,
			buttons: buttons,
			layout: layout,
		})
	}
	if(type === "info"){
		iziToast.info({
			position: 'topRight',
			color: color ? color : 'blue',
			title: title,
			message: str,
			timeout: timeout,
			buttons: buttons,
			layout: layout,
		})
	}
	if(type === "warning"){
		iziToast.warning({
			position: 'topRight',
			color: color ? color : 'yellow',
			title: title,
			message: str,
			timeout: timeout,
			buttons: buttons,
			layout: layout,
		})
	}
	if(type === "error"){
		iziToast.error({
			position: 'topRight',
			color: color ? color : 'red',
			title: title,
			message: str,
			timeout: timeout,
			buttons: buttons,
			layout: layout,
		})
	}
}

const truncate = (str, len=20) => {
	return str.length <= len ? str: (str.substr(0, len)+"...");
}

let have_connected_server = false;
let connect_count_server = 0;

const connectChat = () => {
	connect_count_server++
	const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/")
	const add_chat_log = (message, add_front=false) => {
		const chatWrapElement = document.getElementById("chat-log")
		const dtElement = document.createElement("dt")
		dtElement.innerHTML = `<span class="user" title="${message.send_user.class ? message.send_user.class + "期生" : "その他" }">${message.send_user.display_name}</span>`
		if(message.sender_circle_name){
			dtElement.innerHTML += `<span class='sender-circle' onclick='refreshCircleInfo(${message.sender_circle_pk})'>${message.sender_circle_name}</span>`
		}
		if(message.receiver_circle_name){
			dtElement.innerHTML += `<span class='receiver' onclick='refreshCircleInfo(${message.receiver_circle_pk})'>${message.receiver_circle_name}</span>`
		} else if (message.parent_user_name) {
			dtElement.innerHTML += `<span class='receiver' title="${message.parent_comment}">${message.parent_user_name}</span>`
		}
		const ddElement = document.createElement("dd")
		ddElement.innerHTML = message.comment
		ddElement.innerHTML += "<time>" + message.created_at + "</time>"
		if(add_front){
			chatWrapElement.insertBefore(ddElement, chatWrapElement.firstChild)
			chatWrapElement.insertBefore(dtElement, chatWrapElement.firstChild)
		} else {
			chatWrapElement.appendChild(dtElement)
			chatWrapElement.appendChild(ddElement)
		}
	}


	const addMyQuestion = (question) => {
		const questionElement = document.createElement("div")
		questionElement.setAttribute("id", `myquestion-${question.id}`)
		questionElement.classList.add("question")
		questionElement.innerHTML = `
			<p class="userinfo">
				<span class="sender" title="${question.send_user.class ? question.send_user.class + "期生" : "その他" }">${question.send_user.display_name}</span><span class="receiver">${question.receiver_circle_name}</span>
			</p>
			<p class="comment">
				${question.comment.replace(/\r?\n/g, "<br>")}
			</p>
			<p class="time"><time>${question.created_at}</time></p>
		`
		myQuestionsElement.insertBefore(questionElement, myQuestionsElement.firstChild)
	}

	const addMyQuestionReply = (message) => {
		const parentQuestionElement = document.getElementById(`myquestion-${message.parent_pk}`)
		const replyElement = document.createElement("div")
		replyElement.classList.add("question-reply")
		replyElement.innerHTML = `
			<p class="sender">
				${message.send_user.display_name}
				<span class="sender-circle">${message.sender_circle_name}</span>
			</p>
			<p class="comment">${message.comment}</p>
			<p class="time"><time>${message.created_at}</time></p>
		`
		parentQuestionElement.appendChild(replyElement)
	}


	const addStaffQuestion = (question) => {
		const questionElement = document.createElement("div")
		questionElement.setAttribute("id", `staffquestion-${question.id}`)
		questionElement.classList.add("question")
		questionElement.innerHTML = `
			<p class="userinfo">
				<span class="sender" title="${question.send_user.class ? question.send_user.class + "期生" : "その他" }">${question.send_user.display_name}</span><span class="receiver">${question.receiver_circle_name}</span>
			</p>
			<p class="comment">
				${question.comment.replace(/\r?\n/g, "<br>")}
			</p>
			<p class="time"><time>${question.created_at}</time></p>
		`
		const replyFormElement = document.createElement("form")
		replyFormElement.setAttribute("onsubmit", "return false;")
		replyFormElement.innerHTML = `
			<input type="hidden" value="${question.id}" name="parent">
			<input type="hidden" value="${question.receiver_circle_pk}" name="sender_circle">
			<p><textarea name="comment" required></textarea></p>
			<p><input type="submit"></p>
		`
		replyFormElement.addEventListener("submit", (event) => {
			chatSocket.send(JSON.stringify({"message": {"comment": event.target.comment.value, "parent_pk": parseInt(event.target.parent.value), "sender_circle_pk": parseInt(event.target.sender_circle.value),"is_anonymous": false}}));
			replyFormElement.parentNode.removeChild(replyFormElement);
			const openReplyFormButtonElement = document.querySelector(`#staffquestion-${event.target.parent.value} button`)
			openReplyFormButtonElement.disabled = false
		})
		const openReplyFormButtonElement = document.createElement("button")
		openReplyFormButtonElement.textContent = "返信"
		openReplyFormButtonElement.addEventListener("click", (event) => {
			openReplyFormButtonElement.parentNode.insertBefore(replyFormElement, openReplyFormButtonElement.nextSibling);
			openReplyFormButtonElement.disabled = true
		})
		questionElement.appendChild(openReplyFormButtonElement)
		getQuestionsElement.insertBefore(questionElement, getQuestionsElement.firstChild)
	}


	const addStaffQuestionReply = (message) => {
		const parentQuestionElement = document.getElementById(`staffquestion-${message.parent_pk}`)
		const openReplyFormButtonElement = parentQuestionElement.getElementsByTagName("button")[0]
		const replyElement = document.createElement("div")
		replyElement.classList.add("question-reply")
		replyElement.innerHTML = `
					<p class="sender">${message.send_user.display_name}</p>
					<p class="comment">${message.comment}</p>
					<p class="time"><time>${message.created_at}</time></p>
				`
		parentQuestionElement.insertBefore(replyElement, openReplyFormButtonElement)
	}

	chatSocket.onmessage = function (event) {
		const data = JSON.parse(event.data)
		if(data["initial_messages"]){
			const chatWrapElement = document.getElementById("chat-log")
			chatWrapElement.textContent = ""
			const initial_messages = data["initial_messages"]
			for(const message of initial_messages){
				add_chat_log(message)
			}
			if(have_connected_server){
				show_notify("サーバーとの再接続に成功しました。", {type: "info"})
			}
			have_connected_server = true
			connect_count_server = 0
		}
		if(data["message"]){
			const message = JSON.parse(data["message"]);
			add_chat_log(message, true)
			if(message.is_your_question){
				addMyQuestion(message)
				show_notify(message.receiver_circle_name + "へ質問を送りました。")
			}
			if(message.is_your_answer){
				addMyQuestionReply(message)
				show_notify(message.comment.replace(/\r?\n/g, "<br>"), {
					title: `${message.sender_circle_name}から回答が届きました`,
					timeout: false,
					layout: 2,
					buttons: [["<button>開く</button>", (instance, toast) => {
						openShowMyQuestions()
						staffMode(false)
						document.getElementById(`myquestion-${message.parent_pk}`).scrollIntoView({behavior: "smooth"})
						instance.hide({
							transitionOut: 'fadeOutUp',
							onClosing: function(instance, toast, closedBy){
								console.info('closedBy: ' + closedBy); // The return will be: 'closedBy: buttonName'
							}
						}, toast, 'buttonName');
					}]]
				})
			}
			if(staffCircleIdList.includes(message.sender_circle_pk)){
				addStaffQuestionReply(message)
			}
			if(staffCircleIdList.includes(message.receiver_circle_pk)){
				addStaffQuestion(message)
				show_notify(message.comment.replace(/\r?\n/g, "<br>"), {
					title: circleList[message.receiver_circle_pk].name + "に質問が届きました",
					timeout: false,
					layout: 2,
					buttons: [["<button>開く</button>", (instance, toast) => {
						staffMode(true);
						document.getElementById(`staffquestion-${message.id}`).scrollIntoView({behavior: "smooth"})
						instance.hide({
							transitionOut: 'fadeOutUp',
							onClosing: function(instance, toast, closedBy){
								console.info('closedBy: ' + closedBy); // The return will be: 'closedBy: buttonName'
							}
						}, toast, 'buttonName');
					}]]
				})
			}
		}
	}
	chatSocket.onclose = function (event) {
		chatSendFormElement.removeEventListener("submit", sendComment)
		questionSendFormElement.removeEventListener("submit", sendQuestion)
		getQuestionsElement.textContent = ""
		if(connect_count_server < 6){
			show_notify("サーバーから切断されました。再接続します。", {type: "warning"})
			setTimeout(connectChat, 5000)
		} else {
			show_notify("サーバーと通信できません。時間をおいてページを再読込してみてください。", {type: "error", timeout: false})
		}
	}
	const sendComment = () => {
		const commentElement = document.getElementById("comment");
		chatSocket.send(JSON.stringify({"message": {"comment": commentElement.value, "receiver_circle_pk": null, "is_anonymous": false}}));
		commentElement.value = "";
	}

	const sendQuestion = () => {
		const circleListElement = document.getElementById("circles-question");
		const questionTextElement = document.getElementById("question-text");
		const questionAnonymousElement = document.getElementById("ask-anonymous");
		chatSocket.send(JSON.stringify({"message": {"comment": questionTextElement.value, "receiver_circle_pk": parseInt(circleListElement.value), "is_anonymous": questionAnonymousElement.checked}}));
		questionTextElement.value = "";
	}

	const sendCircleMessage = () => {
		chatSocket.send(JSON.stringify({"message": {"comment": circleMessageSendFormElement.comment.value, "sender_circle_pk": parseInt(circleMessageSendFormElement.circle.value), "is_anonymous": false}}));
		circleMessageSendFormElement.comment.value = ""
	}

	const chatSendFormElement = document.getElementById("chat-send-form");
	chatSendFormElement.addEventListener("submit", sendComment)

	const questionSendFormElement = document.getElementById("circle-question-form");
	questionSendFormElement.addEventListener("submit", sendQuestion)

	if(document.getElementById("circle-message-send-form")){
		const circleMessageSendFormElement = document.getElementById("circle-message-send-form");
		circleMessageSendFormElement.addEventListener("submit", sendCircleMessage)
	}

	const getMyQuestions = () => {
		fetch("api/my_questions")
			.then(function (response) {
				return response.json();
			})
			.then(function (json) {
				if (json.success) {
					for(const question of json.questions){
						addMyQuestion(question)
						for(const reply of question.replies){
							addMyQuestionReply(reply)
						}
					}
				}
			})
	}


	const getStaffQuestions = () => {
		fetch("api/staff_questions")
			.then(function (response) {
				return response.json();
			})
			.then(function (json) {
				if (json.success) {
					for(const question of json.questions){
						addStaffQuestion(question)
						for(const reply of question.replies){
							addStaffQuestionReply(reply)
						}
					}
				}
			})
	}

	const myQuestionsElement = document.getElementById("my-questions")
	getMyQuestions()
	const getQuestionsElement = document.getElementById("get-questions")
	if(document.getElementById("side-wrap-staff")){
		getStaffQuestions()
	}

}


const sendNewName = () => {
	const newNameElement = document.getElementById("new-name")
	const prm = new URLSearchParams();
	prm.append("name",newNameElement.value);
	fetch("/api/user/name/update", {
		method: "POST",
		headers: {"X-CSRFToken": Cookies.get('csrftoken')},
		body: prm,
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (json) {
			if (json.success) {
				const entryWrapElement = document.getElementById("circle-entry")
				entryWrapElement.classList.remove("edit-name")
				const nameElement = document.getElementById("new-name")
				nameElement.value = json.name
			}
		})
}
const sendNewDisplayName = () => {
	const newNameElement = document.getElementById("new-display-name")
	const prm = new URLSearchParams();
	prm.append("name", newNameElement.value);
	fetch("/api/user/display_name/update", {
		method: "POST",
		headers: {"X-CSRFToken": Cookies.get('csrftoken')},
		body: prm,
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (json) {
			if (json.success) {
				const chatWrapElement = document.getElementById("chat-wrap")
				chatWrapElement.classList.remove("edit-name")
				const displayNameElement = document.getElementById("new-display-name")
				displayNameElement.value = json.name
			}
		})
}

const entryCircle = () => {
	const circlesEntryElement = document.getElementById("circles-entry");

	fetch("api/entry/" + circlesEntryElement.value, {
		method: "POST",
		headers: {"X-CSRFToken": Cookies.get('csrftoken')},
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (json) {
			if (json.success) {
				show_notify(json.entered_circle_name + "に入会申し込みしました。")
				const enteredCircleUlElement = document.getElementById("entered_circles")
				enteredCircleUlElement.innerHTML = "";
				for(const circle of json.entry_circles){
					const liElement = document.createElement("li")
					liElement.textContent = circle.name
					liElement.addEventListener("click", () => {
						refreshCircleInfo(circle.id);
					})
					enteredCircleUlElement.appendChild(liElement)
				}
			} else {
				show_notify(json.error, {type:"warning"})
			}
		})
}

const editDisplayName = () => {
	const chatWrapElement = document.getElementById("chat-wrap")
	chatWrapElement.classList.add("edit-name")
}

const refreshCircleInfo = (value=false) => {
	const circlesInfoElement = document.getElementById("circles-info");
	const circlesSelectElements = document.getElementsByClassName("circles-select");
	if(!value){
		value = circlesInfoElement.value
	}
	const circleInfo = circleList[value]
	for(const element of circlesSelectElements){
		element.value = value
	}
	const circleInfoNameElement = document.getElementById("circle-info-name")
	const circleInfoNameDdElement = circleInfoNameElement.getElementsByTagName("dd")[0]
	const circleInfoPanfletElement = document.getElementById("circle-info-panflet")
	const circleInfoPanfletAElement = circleInfoPanfletElement.getElementsByTagName("a")[0]
	const circleInfoWebsiteElement = document.getElementById("circle-info-website")
	const circleInfoWebsiteAElement = circleInfoWebsiteElement.getElementsByTagName("a")[0]
	const circleEntrySubmitWrapElement = document.getElementById("entry-submit-wrap")
	const circleEntryLinkElement = document.getElementById("entry-link")
	circleInfoNameDdElement.textContent = circleInfo.name
	circleInfoPanfletAElement.href = circleInfo.panflet_url
	if(circleInfo.panflet_url !== "None"){
		circleInfoPanfletElement.classList.remove("nodata")
	} else {
		circleInfoPanfletElement.classList.add("nodata")
	}
	circleInfoWebsiteAElement.href = circleInfo.website_url
	if(circleInfo.panflet_url !== "None"){
		circleInfoWebsiteElement.classList.remove("nodata")
	} else {
		circleInfoWebsiteElement.classList.add("nodata")
	}
	if(circleEntrySubmitWrapElement){
		const circleEntryUrl = circleEntryLinkElement.getElementsByTagName("a")[0]
		if(!circleInfo.is_using_entry_form) {
			circleEntrySubmitWrapElement.classList.add("use_outside_form")
			circleEntryUrl.href = circleInfo.entry_form_url
		} else {
			circleEntrySubmitWrapElement.classList.remove("use_outside_form")
			circleEntryUrl.href = "#"
		}
	}
}

const staffMode = (bool) => {
	const sideWrapElement = document.getElementById("side-wrap")
	if(bool) {
		sideWrapElement.classList.add("staff-mode")
	} else {
		sideWrapElement.classList.remove("staff-mode")
	}
}

const toggleShowMyQuestions = () => {
	const circleQuestionElement = document.getElementById("circle-question")
	if(circleQuestionElement.classList.contains("open")){
		circleQuestionElement.classList.remove("open")
	}else{
		circleQuestionElement.classList.add("open")
	}
}
const openShowMyQuestions = () => {
	const circleQuestionElement = document.getElementById("circle-question")
	circleQuestionElement.classList.add("open")
}
const toggleShowEnteredCirles = () => {
	const entryFormElement = document.getElementById("entry-form")
	if(entryFormElement.classList.contains("open")){
		entryFormElement.classList.remove("open")
	}else{
		entryFormElement.classList.add("open")
	}
}

window.onload = () => {
	connectChat()
	const player = videojs('video', {"autoplay": true});
	player.on("error", (err) => {
		console.log(err)
	})
	const circlesSelectElements = document.getElementsByClassName("circles-select");
	for(const element of circlesSelectElements){
		element.addEventListener("change", (event) => {
			refreshCircleInfo(event.target.value)
		})
	}
	const textAreaElements = document.getElementsByTagName("textarea");
	for(const element of textAreaElements){
		element.addEventListener("input", (event) => {
			const target = event.target
			const lineHeight = Number(target.getAttribute("rows"));
			const textHeight = target.value.split("\n").length;
			if(target.scrollHeight !== lineHeight){
				if(textHeight < 2){
					target.setAttribute("rows", 2)
				}else if(textHeight <= 10){
					target.setAttribute("rows", textHeight)
				}else{
					target.setAttribute("rows", 10)
				}
			}
		})
	}
	refreshCircleInfo()
}