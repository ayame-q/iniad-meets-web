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
			is_admin: false,
			entered_circles: [],
		},
		isOpen: false,
		socket: null,
		isSocketConnected: false,
		tryConnectSocketCount: 0,
		events: [],
		pastEvents: [],
		chatLogs: [],
		questionResponses: [],
		circles: [],
		reactionEmojis: ["😀", "😆", "😅", "🤣", "😍", "☺️", "😉", "🥳", "🥺", "🤗", "🤔", "👏", "🤝", "👍", "🙏", "👀", "🙋", "🙇", "🍩", "💕", "⁉️", "✔️", "💯", "🆗", "🆖"],
		chatLogWrapScrolledAt: null,
		isChatLogWrapScrollOnAuto: false,
		chatFormParentUuid: null,
		chatLogForYouReadUuid: localStorage.getItem("chatLogForYouRead"),
		startedTime: null,
		status: {
			status: null,
			final_questionnaire_url: null,
		}
	},
	getters: {
		getSocket(state) {
			return state.socket
		},
		getEvent(state) {
			return state.pastEvents[state.pastEvents.length - 1]
		},
		getEvents(state) {
			return state.events
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
		getMyEnteredCircles(state) {
			return state.myUser.entered_circles
		},
		getNowCircle(state, getters) {
			try {
				return state.circles.find((item) => {
					return item.uuid === getters.getEvent.circle
				})
			} catch (e) {
				return null
			}
		},
		getNextCircle(state, getters) {
			if (!getters.getNowCircle) {
				const pastEvents = state.pastEvents
				for (let i = pastEvents.length - 1; i >= 0; i--) {
					if (pastEvents[i].type === "circle_start") {
						const lastCircle = state.circles.find((item) => {
							return item.uuid === pastEvents[i].circle
						})
						const index = state.circles.indexOf(lastCircle)
						return state.circles[index + 1]
					}
				}
				return state.circles[0]
			}
			const index = state.circles.indexOf(getters.getNowCircle) + 1
			return state.circles[index]
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
		getChatLogsForYouNotRead(state, getters) {
			const myChatLog = getters.getChatLogsForYou
			const readChatLog = myChatLog.find((item) => {
				return item.uuid === state.chatLogForYouReadUuid
			})
			const index = myChatLog.indexOf(readChatLog)
			return myChatLog.slice(index + 1)
		},
		getChatLogsQuestionsAndAnswers(state) {
			return state.chatLogs.filter((item) => {
				return (item.is_question || item.is_answer)
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
		},
		getQuestionResponses(state) {
			return state.questionResponses
		},
		getStatus(state) {
			return state.status
		}
	},
	mutations: {
		setSocket(state, socket) {
			state.socket = socket
		},
		setStatus(state, status) {
			state.status = status
		},
		setStartedTimeNow(state) {
			state.startedTime = dayjs()
		},
		setStartedTimeBeforeMillisec(state, millisec) {
			state.startedTime = dayjs().subtract(millisec, "ms")
		},
		setMyUser(state, user) {
			state.myUser = user
		},
		setEvents(state, events) {
			state.events = events
		},
		setPastEvents(state) {
			if (!state.startedTime){
				return null
			}
			state.pastEvents = state.events.filter((item) => {
				return state.startedTime.add(item.start_time_sec, "s") <= dayjs()
			})
		},
		setCircles(state, circles){
			state.circles = circles
		},
		addEnteredCircle(state, circle) {
			state.myUser.entered_circles.push(circle)
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
		setQuestionResponses(state, responses) {
			state.questionResponses = responses
		},
		addQuestionResponse(state, response) {
			const original = state.questionResponses.filter((item) => {
				item.question_uuid === response.question_uuid
			})
			if (original){
				state.questionResponses.splice(state.questionResponses.indexOf(original), 1)
			}
			state.questionResponses.push(response)
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
		setChatLogForYouRead(state, uuid) {
			state.chatLogForYouReadUuid = uuid
			localStorage.setItem(`chatLogForYouRead`, uuid)
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

			const socket = new WebSocket(process.env.VUE_APP_WEBSOCKET_PROTOCOL + "://" + window.location.host + "/ws/chat/")

			const jsonReviver = (key, val) => {
				if (typeof(val) == "string" &&
					val.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?\+\d{2}:\d{2}$/)){
					return dayjs(val);
				}
				return val;
			}

			socket.onmessage = (event) => {
				const response = JSON.parse(event.data, jsonReviver)

				for (const [event, data] of Object.entries(response)) {
					//console.log("Get WebSocket message:", event, data)
					if (event === "start") {
						context.commit("setStartedTimeNow")
						for (const event of context.getters.getEvents) {
							setTimeout((() => {
								context.commit("setPastEvents")
							}), event.start_time_sec * 1000)
						}
					} else if (event === "init") {
						context.commit("setSocketConnected")
						if (data.started_before_millisec){
							context.commit("setStartedTimeBeforeMillisec", data.started_before_millisec)
						}
						context.commit("setCircles", data.circles)
						context.commit("setEvents", data.events)
						context.commit("setPastEvents")
						for (const event of context.getters.getEvents) {
							if (data.started_before_millisec / 1000 < event.start_time_sec)
							setTimeout((() => {
								context.commit("setPastEvents")
								if (event.type === "question_result" && event.question.type === 2) {
									context.dispatch("getEventUpdated")
								}
							}), event.start_time_sec * 1000 - data.started_before_millisec)
						}
						context.commit("setMyUser", data.user)
						context.commit("setChatLogs", data.chat_logs)
						context.commit("setQuestionResponses", data.question_responses)
						context.commit("setStatus", data.status)
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
					} else if (event === "events") {
						context.commit("setEvents", data)
						context.commit("setPastEvents")
					} else if (event === "question_response") {
						context.commit("addQuestionResponse", data)
					} else if (event === "user") {
						context.commit("setMyUser", data)
					}
				}
			}

			socket.onclose = (event) => {
				context.commit("setSocketDisconnected")
				console.log("Disconnect from websocket server. Reconnect later.")
				setTimeout(() => {
					context.dispatch("connectWebSocket")
				}, 5000)
			}

			socket.onerror = (error) => {
				console.error(error)
				socket.close()
			}

			context.commit("setSocket", socket)
		},
		sendSocket(context, {event, data}) {
			const socket = context.getters.getSocket
			socket.send(JSON.stringify(({
				[event]: data
			})))
			//console.log("Send Websocket Message", event, data)
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
		},
		sendQuestionResponse(context, uuid) {
			context.dispatch("sendSocket", {
				event: "question_response",
				data: {
					uuid: uuid
				}
			})
		},
		getEventUpdated(context) {
			context.dispatch("sendSocket", {
				event: "get_events_updated",
				data: true
			})
		},
		sendStart(context) {
			context.dispatch("sendSocket", {
				event: "start",
				data: true
			})
		},
		updateDisplayName(context, displayName) {
			context.dispatch("sendSocket", {
				event: "update_display_name",
				data: {
					display_name: displayName
				}
			})
		}
	},
	modules: {},
});
