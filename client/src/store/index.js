import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import dayjs from "dayjs";

Vue.use(Vuex);

export default new Vuex.Store({
	state: {
		myUser: {
			uuid: null,
			staff_circles: [],
			is_admin: false
		},
		isOpen: false,
		socket: null,
		isSocketConnected: false,
		tryConnectSocketCount: 0,
		chatLogs: [],
		questions: [],
		circles: [],
		reactionEmojis: ["😀", "😆", "😅", "🤣", "😍", "☺️", "😉", "🥳", "🥺", "🤗", "🤔", "👏", "🤝", "👍", "🙏", "👀", "🙋", "🙇", "🍩", "💕", "⁉️", "✔️", "💯", "🆗", "🆖"],
		chatLogWrapScrolledAt: null,
		isChatLogWrapScrollOnAuto: false,
		chatFormParentUuid: null,
	},
	getters: {
		getSocket(state) {
			return state.socket
		},
		getMyUser(state) {
			return state.myUser
		},
		getMyUuid(state) {
			return state.myUser.uuid
		},
		getCircles(state) {
			return state.circles
		},
		getIsAdmin(state) {
			return state.myUser.is_admin
		},
		getMyStaffCircles(state) {
			return state.myUser.staff_circles
		},
		getChatLogs(state) {
			return state.chatLogs
		},
		getChatLogsAdminMessages(state) {
			return state.chatLogs.filter((item) => {
				return item.is_admin_message
			})
		},
		getChatLogsForYou(state) {
			return state.chatLogs.filter((item) => {
				return (
					(item.receiver_user && item.receiver_user.uuid === state.myUser.uuid) ||
					(item.receiver_circle && state.myUser.staff_circles.some((myCircleItem) => {
						return myCircleItem.uuid === item.receiver_circle.uuid
					}))
				)
			})
		},
		getChatLogsQuestionsAndAnswers(state) {
			return state.chatLogs.filter((item) => {
				return (item.is_question || item.is_answer)
			})
		},
		getQuestions(state) {
			return state.questions
		},
		getQuizzes(state) {
			return state.questions.filter((item, index) => {
				return item.type === 1
			})
		},
		getQuestionnaire(state) {
			return state.questions.filter((item, index) => {
				return item.type === 2
			})
		},
		getIsSocketConnected(state) {
			return state.isSocketConnected
		},
		getTryConnectSocketCount(state) {
			return state.tryConnectSocketCount
		},
		getReactionEmojis(state) {
			return state.reactionEmojis
		},
		getChatLogWrapScrolledAt(state) {
			return state.chatLogWrapScrolledAt
		},
		getChatFormParentUuid(state) {
			return state.chatFormParentUuid
		}
	},
	mutations: {
		setSocket(state, socket) {
			state.socket = socket
		},
		setMyUser(state, user) {
			state.myUser = user
		},
		setCircles(state, circles){
			state.circles = circles
		},
		setChatLogs(state, logs) {
			state.chatLogs = logs
		},
		addChatLog(state, log) {
			state.chatLogs.push(log)
		},
		addChatLogsOld(state, logs){
			state.chatLogs = logs.concat(state.chatLogs)
		},
		addChatReaction(state, reaction) {
			const chatLog = state.chatLogs.find((item) => {
				return item.uuid === reaction.chat_log_uuid
			})
			chatLog.reactions.push(reaction)
		},
		removeChatReaction(state, reaction) {
			const chatLog = state.chatLogs.find((item) => {
				return item.uuid === reaction.chat_log_uuid
			})
			chatLog.reactions = chatLog.reactions.filter((item) => {
				return item.uuid !== reaction.uuid
			}) // 指定されたリアクションを削除
		},
		setQuestions(state, questions) {
			state.questions = questions
		},
		addQuestion(state, question) {
			state.questions.push(question)
		},
		setSocketConnected(state) {
			state.tryConnectSocketCount = 0
			state.isSocketConnected = true
		},
		setSocketDisconnected(state) {
			state.isSocketConnected = false
		},
		setSocketTry(state) {
			state.tryConnectSocketCount++
		},
		startChatLogWrapScrollAuto(state) {
			state.isChatLogWrapScrollOnAuto = true
		},
		endChatLogWrapScrollAuto(state) {
			state.isChatLogWrapScrollOnAuto = false
		},
		setChatLogWrapScrolledAt(state) {
			if (!state.isChatLogWrapScrollOnAuto) {
				state.chatLogWrapScrolledAt = dayjs()
			}
		},
		clearChatLogWrapScrolledAt(state) {
			state.chatLogWrapScrolledAt = null
		},
		setChatFormParentUuid(state, parentUuid) {
			state.chatFormParentUuid = parentUuid
		}
	},
	actions: {
		checkIsOpen(context) {
			axios.get("/api/isopen")
		},
		connectWebSocket(context) {
			context.commit("setSocketTry") // 接続試行を記録

			if (context.getters.getIsSocketConnected > 5) {
				return 1
			}

			const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/")

			const jsonReviver = (key, val) => {
				if (typeof(val) == "string" &&
					val.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?\+\d{2}:\d{2}$/)){
					return dayjs(val);
					//2021-04-16T10:59:32+00:00
				}
				return val;
			}

			socket.onmessage = (event) => {
				const response = JSON.parse(event.data, jsonReviver)

				for (const [event, data] of Object.entries(response)) {
					console.log("Get WebSocket message:", event, data)
					if (event === "init") {
						context.commit("setSocketConnected")
						context.commit("setMyUser", data.user)
						context.commit("setCircles", data.circles)
						context.commit("setChatLogs", data.chat_logs)
						context.commit("setQuestions", data.questions)
					} else if (event === "chat_message") {
						context.commit("addChatLog", data)
					} else if (event === "chat_reaction_add") {
						context.commit("addChatReaction", data)
					} else if (event === "chat_reaction_remove") {
						context.commit("removeChatReaction", data)
					} else if (event === "question") {
						context.commit("addQuestion", data)
					} else if (event === "old_messages") {
						context.commit("addChatLogsOld", data.chat_logs)
						setTimeout(() => {
							const keyChatLogElement = document.getElementById("chat-log-" + data.start_message_uuid)
							if (keyChatLogElement) {
								keyChatLogElement.scrollIntoView()
							}
						})
					}
				}
			}

			socket.onclose = (event) => {
				context.commit("setSocketDisconnected")
				setTimeout(context.dispatch("connectWebSocket"), 5000)
			}

			context.commit("setSocket", socket)
		},
		sendSocket(context, {event, data}) {
			const socket = context.getters.getSocket
			socket.send(JSON.stringify(({
				[event]: data
			})))
			console.log("Send Websocket Message", event, data)
		},
		sendChatMessage(context, {comment, parent=null, senderCircleUuid=null, receiverCircleUuid=null, isAnonymous=false, isAdminMessage=false}) {
			context.dispatch("sendSocket", {
				event: "chat_message",
				data: {
					"comment": comment,
					"parent": parent,
					"sender_circle_uuid": senderCircleUuid,
					"receiver_circle_uuid": receiverCircleUuid,
					"is_anonymous": isAnonymous,
					"is_admin_message": isAdminMessage
				}
			})
		},
		addChatReaction(context, {messageUuid, reaction}) {
			context.dispatch("sendSocket", {
				event: "chat_reaction_add",
				data: {
					"message_uuid": messageUuid,
					"reaction": reaction,
				}
			})
		},
		removeChatReaction(context, {messageUuid, reaction}) {
			context.dispatch("sendSocket", {
				event: "chat_reaction_remove",
				data: {
					"message_uuid": messageUuid,
					"reaction": reaction,
				}
			})
		},
		getOldMessages(context) {
			const oldestMessageUuid = context.getters.getChatLogs[0].uuid
			context.dispatch("sendSocket", {
				event: "get_old_messages",
				data: {
					oldest_uuid: oldestMessageUuid
				}
			})
		}
	},
	modules: {},
});
