const show_notify = (str, arr={}) => {
	type = arr.type ? arr.type : "normal"
	arr.message = str
	if(!arr.position){
		arr.position =  'topRight'
	}
	if(type === "normal"){
		if(!arr.color){
			arr.color = 'blue'
		}
		return iziToast.show(arr)
	}
	if(type === "info"){
		if(!arr.color){
			arr.color = 'green'
		}
		return iziToast.info(arr)
	}
	if(type === "warning"){
		if(!arr.color){
			arr.color = 'yellow'
		}
		return iziToast.warning(arr)
	}
	if(type === "error"){
		if(!arr.color){
			arr.color = 'red'
		}
		return iziToast.error(arr)
	}
}

const truncate = (str, len=20) => {
	return str.length <= len ? str: (str.substr(0, len)+"...");
}

let have_connected_server = false;
let connect_count_websocket_server = 0;
let yongest_log_id = -1;

const connectChat = () => {
	connect_count_websocket_server++
	const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/")
	const add_chat_log = (message, add_front=false) => {
		if(yongest_log_id < 0 || yongest_log_id > message.id){
			yongest_log_id = message.id
		}
		const chatWrapElement = document.getElementById("chat-log")
		const dtElement = document.createElement("dt")
		dtElement.innerHTML = `<span class="user" title="${message.send_user.class ? message.send_user.class + "期生" : "その他" }">${message.send_user.display_name}</span>`
		if(message.sender_circle_name){
			dtElement.innerHTML += `<span class='sender-circle' onclick='showCircleInfo(${message.sender_circle_pk})'>${message.sender_circle_name}</span>`
		}
		if(message.receiver_circle_name){
			dtElement.innerHTML += `<span class='receiver' onclick='showCircleInfo(${message.receiver_circle_pk})'>${message.receiver_circle_name}</span>`
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
			yongest_log_id = -1
			const initial_messages = data["initial_messages"]
			for(const message of initial_messages){
				add_chat_log(message)
			}
			if(have_connected_server){
				show_notify("サーバーとの再接続に成功しました。", {type: "info"})
				getStatus()
			}
			have_connected_server = true
			connect_count_websocket_server = 0
		}

		if(data["old_messages"]){
			const chatWrapElement = document.getElementById("chat-log")
			const old_messages = data["old_messages"]
			for(const message of old_messages){
				if(message.id < yongest_log_id){
					add_chat_log(message)
				}
			}
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
						mobileTab("info")
						staffMode(false)
						document.getElementById(`myquestion-${message.parent_pk}`).scrollIntoView({behavior: "smooth"})
						instance.hide({
							transitionOut: 'fadeOutUp',
							onClosing: () => {}
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
						mobileTab("info")
						staffMode(true);
						document.getElementById(`staffquestion-${message.id}`).scrollIntoView({behavior: "smooth"})
						instance.hide({
							transitionOut: 'fadeOutUp',
							onClosing: () => {}
						}, toast, 'buttonName');
					}]]
				})
			}
		}

		if(data["notify"]){
			const notify = JSON.parse(data["notify"])
			show_notify(notify.comment, {type: notify.type, timeout: notify.timeout, color: notify.color})
		}

		if(data["start_broadcast"]){
			if(is_video_error || is_video_waiting){
				window.location.reload()
			}
		}

		if(data["status"]){
			const status = JSON.parse(data["status"])
			updateStatus(status)
		}

		if(data["force_reload"]){
			window.location.reload()
		}

	}
	chatSocket.onclose = function (event) {
		chatSendFormElement.removeEventListener("submit", sendComment)
		questionSendFormElement.removeEventListener("submit", sendQuestion)
		if(document.getElementById("circle-message-send-form")){
			const circleMessageSendFormElement = document.getElementById("circle-message-send-form");
			circleMessageSendFormElement.removeEventListener("submit", sendCircleMessage)
		}
		if(getQuestionsElement){
			getQuestionsElement.textContent = ""
		}
		if(connect_count_websocket_server < 6){
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
		const circleMessageSendFormElement = document.getElementById("circle-message-send-form");
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
	const chatLogWrapElement = document.getElementById("chat-log-wrap")
	chatLogWrapElement.addEventListener("scroll", () => {
		if(chatLogWrapElement.scrollHeight - chatLogWrapElement.scrollTop === chatLogWrapElement.clientHeight){
			chatSocket.send(JSON.stringify({"get_old": yongest_log_id}))
		}
	})

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
const sendNewDisplayName = (event) => {
	const newName = event.target.displayName.value
	const prm = new URLSearchParams();
	prm.append("name", newName);
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
				const editElements = document.getElementsByClassName("edit-display-name")
				const displayNameFormElements = document.getElementsByClassName("display-name-form")
				for(const element of editElements){
					element.classList.remove("edit-display-name")
				}
				for(const element of displayNameFormElements){
					element.displayName.value = json.name
				}
			}
		})
}

const entryCircle = () => {
	const circlesEntryElement = document.getElementById("circles-entry");
	const entryCircleID = circlesEntryElement.value

	show_notify(`${circleList[entryCircleID].name}に入会申込しますか？`, {
		timeout: false,
		drag: false,
		buttons: [
			["<button>はい</button>", (instance, toast) => {
				instance.hide({
					transitionOut: 'fadeOutUp',
					onClosing: () => {},
				}, toast, 'buttonName');

				fetch("api/entry/" + entryCircleID, {
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
									showCircleInfo(circle.id);
								})
								enteredCircleUlElement.appendChild(liElement)
							}
						} else {
							show_notify(json.error, {type:"warning"})
						}
					})
			}],
			["<button>キャンセル</button>", (instance, toast) => {
				instance.hide({
					transitionOut: 'fadeOutUp',
					onClosing: () => {
					},
				}, toast, 'buttonName');
			}]
		],
		onOpening: (instance, toast) => {
			first_message = toast
		},
	})



}

const editName = () => {
	show_notify("事務課への提出に必要なため、<br>入会フォームの氏名欄には必ず<br>本名をフルネームで入力してください。<br><small>(あなたが入会したサークルの担当者以外に公開することは<br>ありませんのでご安心ください。)</small>", {targetFirst: false, timeout: 25000})
	const chatWrapElement = document.getElementById("circle-entry")
	chatWrapElement.classList.add("edit-name")
}

const editDisplayName = () => {
	const chatWrapElement = document.getElementById("chat-wrap")
	chatWrapElement.classList.add("edit-display-name")
}

const showCircleInfo = (value=false) => {
	const circlesInfoElement = document.getElementById("circles-info");
	if(!value){
		value = circlesInfoElement.value
	}
	const circleInfo = circleList[value]
	const circlesSelectElements = document.getElementsByClassName("circles-select");
	const questionTextElement = document.getElementById("question-text");
	for(const element of circlesSelectElements){
		if(element.id !== "circles-question"){
			element.value = value
		}else{
			if(questionTextElement.value === ""){
				element.value = value
			}
		}
	}
	const circleInfoStartTimeElement = document.getElementById("circle-info-start-time")
	const circleInfoStartTimeTimeElement = circleInfoStartTimeElement.getElementsByTagName("time")[0]
	const circleInfoCommentElement = document.getElementById("circle-info-comment")
	const circleInfoCommentPElement = circleInfoCommentElement.getElementsByTagName("p")[0]
	const circleInfoPanfletElement = document.getElementById("circle-info-panflet")
	const circleInfoPanfletAElement = circleInfoPanfletElement.getElementsByTagName("a")[0]
	const circleInfoWebsiteElement = document.getElementById("circle-info-website")
	const circleInfoWebsiteAElement = circleInfoWebsiteElement.getElementsByTagName("a")[0]
	const circleInfoTwitterElement = document.getElementById("circle-info-twitter")
	const circleInfoTwitterAElement = circleInfoTwitterElement.getElementsByTagName("a")[0]
	const circleInfoTwitterSnElement = document.getElementById("circle-info-twitter_sn")
	const circleEntrySubmitWrapElement = document.getElementById("entry-submit-wrap")
	const circleEntryLinkElement = document.getElementById("entry-link")
	circleInfoStartTimeTimeElement.textContent = circleInfo.start_time_str
	if(circleInfo.start_time_str){
		circleInfoStartTimeElement.classList.remove("nodata")
	} else {
		circleInfoStartTimeElement.classList.add("nodata")
	}
	circleInfoCommentPElement.innerHTML = circleInfo.comment.replace(/\r?\n/g, "<br>")
	if(circleInfo.comment){
		circleInfoCommentElement.classList.remove("nodata")
	} else {
		circleInfoCommentElement.classList.add("nodata")
	}
	circleInfoPanfletAElement.href = circleInfo.panflet_url
	if(circleInfo.panflet_url){
		circleInfoPanfletElement.classList.remove("nodata")
	} else {
		circleInfoPanfletElement.classList.add("nodata")
	}
	circleInfoWebsiteAElement.href = circleInfo.website_url
	if(circleInfo.website_url){
		circleInfoWebsiteElement.classList.remove("nodata")
	} else {
		circleInfoWebsiteElement.classList.add("nodata")
	}
	circleInfoTwitterAElement.href = "https://twitter.com/" + circleInfo.twitter_sn
	circleInfoTwitterSnElement.textContent = circleInfo.twitter_sn
	if(circleInfo.twitter_sn){
		circleInfoTwitterElement.classList.remove("nodata")
	} else {
		circleInfoTwitterElement.classList.add("nodata")
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
		const circleEntryElement = document.getElementById("circle-entry")
		if(!circleInfo.is_using_entry_form && !circleInfo.entry_form_url){
			circleEntryElement.classList.add("cannot-entry")
		}else{
			circleEntryElement.classList.remove("cannot-entry")
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
const mobileTab = (mode) => {
	const sideWrapElement = document.querySelector("main")
	if(mode === "chat") {
		sideWrapElement.classList.add("chat-mode")
	} else {
		sideWrapElement.classList.remove("chat-mode")
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
	const entryFormElement = document.getElementById("entry-form-wrap")
	if(entryFormElement.classList.contains("open")){
		entryFormElement.classList.remove("open")
	}else{
		entryFormElement.classList.add("open")
	}
}

const showTutorial = () => {
	setTimeout(() => {
		show_notify("ご参加ありがとうございます！", {targetFirst: false, timeout: 10000})
	}, 1000)
	setTimeout(() => {
		show_notify("画面右側にはサークルの簡単な情報があります。<br>また、各サークルへの質問や、<br>各サークルに簡単に入会申し込みすることができます！", {targetFirst: false, timeout: 25000})
	}, 3000)
	setTimeout(() => {
		show_notify("なお、事務課への提出に必要なため、<br>右下の入会フォームの氏名欄には必ず<br>本名をフルネームで入力してください。<br><small>(あなたが入会したサークルの担当者以外に<br>公開することはありませんのでご安心ください。)</small>", {targetFirst: false, timeout: 25000})
	}, 5000)
	setTimeout(() => {
		show_notify("画面左下にはチャットがあります！<br>好きな公開名を登録して<br>チャットでの会話を楽しんでください。<br>ちょっとした会話も大歓迎です！", {targetFirst: false, timeout: 25000})
	}, 12000)
	setTimeout(() => {
		show_notify("もし気になることがございましたら、<br>ぜひ右側の質問フォームから<br>お気軽に質問してください。<br>匿名でも質問できます！", {targetFirst: false, timeout: 25000})
	}, 14000)
	setTimeout(() => {
		show_notify("それでは、短い間ではありますが<br>イベントをお楽しみください！", {targetFirst: false, timeout: 25000})
	}, 20000)
}

let initial_play = true
let is_video_error = false
let is_video_waiting = false
let time_out_waiting_notifies = []
let waiting_notify

const connectVideo = () => {
	let first_message
	const player = videojs('video');
	player.on("error", (err) => {
		is_video_error = true
		show_notify("現在配信されていないようです。配信開始までしばらくお待ちください。<br><small>(配信中のはずなのにこのメッセージが表示される場合は時間をおいて再読込してみてください。)</small>", {type: "error", timeout: false})
	})
	player.on("waiting", () => {
		is_video_waiting = true
		if(!waiting_notify && !is_video_error){
			time_out_waiting_notifies.push(setTimeout(() => {
				show_notify("動画サーバーから切断されました…しばらくお待ちください。", {type: "warning", timeout: 17000,
					onOpening: (instance, toast) => {
						waiting_notify = toast
					},
				})
			}, 3000))
			time_out_waiting_notifies.push(setTimeout(() => {
				is_video_error = true
				iziToast.hide({}, waiting_notify)
				show_notify("動画サーバーと再接続できませんでした。<br>現在配信されていないか、サーバーやネットワーク等の問題が起こっている可能性があります。<br>再読込してみてください。", {type: "error", timeout: false,
					onOpening: (instance, toast) => {
						waiting_notify = toast
					},
				})
			}, 20000))
		}
	})
	player.on("playing", () => {
		is_video_waiting = false
		for(const timeout of time_out_waiting_notifies){
			clearTimeout(timeout)
		}
		if(waiting_notify){
			try{
				iziToast.hide({}, waiting_notify)
			}catch(e){

			}
			show_notify("動画サーバーと再接続しました", {type: "info"})
			waiting_notify = null
		}
	})
	player.on("play", (arg) => {
		if(initial_play){
			try{
				iziToast.hide({}, first_message)
			}catch(e){

			}
		}
		initial_play = false
	})
	player.on("durationchange", () => {
		if(!is_video_error){
			show_notify("INIAD meets Webへようこそ！再生ボタンを押して参加しましょう！", {
				timeout: 180000,
				buttons: [["<button>再生</button>", (instance, toast) => {
					player.play()
					instance.hide({
						transitionOut: 'fadeOutUp',
						onClosing: () => {},
					}, toast, 'buttonName');
				}]],
				onOpening: (instance, toast) => {
					first_message = toast
				},
			})
		}
	})
}

let circleList = {}
let activeCircleSetTimeOutIds = []

const updateStatus = (obj) => {
	circleList = obj.circle_list
	const circlesSelectElements = document.getElementsByClassName("circles-select");
	for(const element of circlesSelectElements){
		element.addEventListener("change", (event) => {
			showCircleInfo(event.target.value)
		})
	}
	const displayNameFormElements = document.getElementsByClassName("display-name-form")
	for(const element of displayNameFormElements){
		element.addEventListener("submit", sendNewDisplayName)
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
	showCircleInfo()
	const sideWrapElement = document.getElementById("side-wrap")
	sideWrapElement.classList.remove("no-circles-info")
	for(const timeOutID of activeCircleSetTimeOutIds){
		clearTimeout(timeOutID)
	}
	for(const key of Object.keys(circleList)){
		const circle = circleList[key]
		const now = new Date().getTime()
		if(circle.start_time_ts && now < circle.start_time_ts){
			activeCircleSetTimeOutIds.push(setTimeout(() => {
				showCircleInfo(circle.id)
			}, circle.start_time_ts - now))
		}
	}
}

const getStatus = () => {
	fetch("api/status")
		.then(function (response) {
			return response.json();
		})
		.then(function (json) {
			updateStatus(json)
		})
}

window.onload = () => {
	getStatus()
	connectChat()
	connectVideo()
}