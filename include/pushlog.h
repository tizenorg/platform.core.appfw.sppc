/*
 * Copyright (c) 2000 - 2012 Samsung Electronics Co., Ltd All Rights Reserved
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * pushlog.h
 *
 *  Created on: Dec 17, 2012
 *      Author: sampath
 */

#ifndef PUSHLOG_H_
#define PUSHLOG_H_


#include <errno.h>
#include <app.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Enumerations of error codes for push log service
 */

typedef enum
{
 	PUSHLOG_ERROR_NONE = 1000,

	// Server reply error code. This should be synchronized with local_msg.h
	PUSHLOG_ERROR_SUCCESS=1000,
	PUSHLOG_ERROR_SUCCESS_AND_NO_UPDATE=1010,	//this is not neccessary in client side. this rc will be replaced to 1000
 	PUSHLOG_ERROR_WRONG_REQUEST_FORMAT=2001,
 	PUSHLOG_ERROR_BLOCKED_DEVICE_TOKEN=2002,
 	PUSHLOG_ERROR_TOO_LONG_REQUEST_MSG=2003,
 	PUSHLOG_ERROR_EXCEEDED_DAILY_QUOTA=2004,
	PUSHLOG_ERROR_FAIL_TO_AUTHENTICATE = 3001,

 	PUSHLOG_ERROR_WRONG_APP_ID = 4010,
 	PUSHLOG_ERROR_EMPTY_SERVICE = 4013,
 	PUSHLOG_ERROR_EMPTY_MESSAGES = 4014,

	PUSHLOG_ERROR_NETWORK_NOT_AVAILABLE = -2,
	PUSHLOG_ERROR_INVALID_REQUEST = -200,
	PUSHLOG_ERROR_LOG_SIZE_OVER = -202,
	PUSHLOG_ERROR_INVALID_LOG_STATUS = -204,
	PUSHLOG_ERROR_ALREADY_REQUESTED = -205,
	PUSHLOG_ERROR_LOGGING_FAIL = -206,
	PUSHLOG_ERROR_REQUEST_TURN_OVER = -207,
	PUSHLOG_ERROR_LOG_NOT_ACTIVATION = -208,

	PUSHLOG_ERROR_INVALID_PARAMETER = -1000,
	PUSHLOG_ERROR_OUT_OF_MEMORY,
	PUSHLOG_ERROR_OPERATION_FAILED,
	PUSHLOG_ERROR_CONNECT_FAIL,
	PUSHLOG_ERROR_INTERNAL_SERVER_ERROR=8002,
	PUSHLOG_ERROR_PANIC=9999
} pushlog_error_e;


/**
 * @brief Enumerations of registration state
 */
typedef enum {
	PUSHLOG_STATE_CONNECTED,   /**< Connected to SPPCD */
	PUSHLOG_STATE_DISCONNECTED, /**< Disconnected from SPPCD */
	PUSHLOG_STATE_READY,
	PUSHLOG_STATE_ERROR,       /**< Error */
} pushlog_state_e;


/**
 * @brief Push log service handle
 */
typedef struct pushlog_connection_s *pushlog_connection_h;


/**
 * @brief Push log data handle
 */
typedef void *pushlog_data;

/**
 * @brief Notification callback for logging service status
 * @param[in] log_req_type status of logging service
 * @param[in] result error code if any.
 * PUSHLOG_ERROR_NONE indicates success.
 * @param[in] user_data User data set with pushlog_connect()
 * @see pushlog_connect()
 */
typedef void (*pushlog_state_cb)(
		pushlog_state_e state, pushlog_error_e err,
		void *user_data);

/**
 * @brief Notification callback invoked for pushlog_send_data() api response
 * @param[in] log_id log id set while sending the data
 * @param[in] result  error code if any.
 * PUSHLOG_ERROR_NONE indicates success.
 * @param[in] user_data User data set with pushlog_connect()
 * @see pushlog_connect()
 */
typedef void (*pushlog_send_cb)(
		const char *log_id, pushlog_error_e err,
		void *user_data);

/**
 * @brief Connects to the push log service and sets callback functions
 * @remarks The status of connection between an application and the push log service,
 * is indicated with the callback push_log_status_cb.
 * Connection should be freed with @ref pushlog_disconnect() by you.
 * @param[in] status_cb connection status callback
 * @param[in] send_cb callback to receive pushlog_send_data() response
 * @param[in] user_data User data to pass to <I>state_cb</I> and <I>notify_cb</I>
 * @param[in] service A @ref Service handle to launch an application by
 * an posted UI notification
 * @param[out] log_h  Handle of a connection to the push log service
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 * @see push_disconnect()
 */
pushlog_error_e pushlog_connect(const char *service_name,
		pushlog_state_cb status_cb,
		pushlog_send_cb send_cb,
		void *cb_data, app_control_h service,
		pushlog_connection_h *log_h);

/**
 * @brief Disconnect push log service
 * @remarks If there is a connection between an application and the push service,
 * the notify callback passes the notification upon its arrival.
 * Otherwise, the push service posts a UI notification to alert users.
 * Connection should be freed with @ref push_disconnect() by you.
 * @param[in] log_h  Handle of a connection to the push log service
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 * @see pushlog_connect()
 */
pushlog_error_e pushlog_disconnect(pushlog_connection_h log_h);

/**
 * @brief Send log data to server
 * @remarks
 * @param[in] log_h  Handle of a connection to the push log service
 * @param[in] log_prefix Data setting for prefix of log.
 * @param[in] log_id log id
 * @param[in] data_h Data to be sent
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_send(pushlog_connection_h log_h,
		const char *log_prefix,
		const char *log_id, pushlog_data data_h);


/**
 * @brief Get push log service's configurations
 * @remarks
 * @param[in] log_h Handle of a connection to the push log service
 * @param[in] item_size
 * @param[out] unlimited_sending
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_get_config(pushlog_connection_h log_h,
		int *item_size, bool *unlimited_sending);

/**
 * @brief
 * @remarks
 * @param[in] log_h Handle of a connection to the push log service
 * @param[in] state
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_get_state(pushlog_connection_h log_h,
				pushlog_state_e *state);

/**
 * @brief
 * @remarks
 * @param[in] data
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_create_data(pushlog_data *data);

/**
 * @brief
 * @remarks
 * @param[in] data
 * @param[in] value
 * @param[in] len
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_add_data(pushlog_data data, char *value, int len);

/**
 * @brief
 * @remarks
 * @param[in] data
 * @return PUSHLOG_ERROR_NONE on success, otherwise a indicated by push_log_error_e.
 */
pushlog_error_e pushlog_free_data(pushlog_data data);


#ifdef __cplusplus
}
#endif

#endif /* PUSHLOG_H_ */
