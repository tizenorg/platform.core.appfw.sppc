//
// Copyright (c) 2012-2013 Samsung Electronics Co., Ltd.
//
// Licensed under the Flora License, Version 1.1 (the License);
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://floralicense.org/license/
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an AS IS BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#ifndef __PUSH_LIB_H__
#define __PUSH_LIB_H__

#include <errno.h>
#include <app.h>

#define PUSH_APP_DATA_KEY  "http://tizen.org/appcontrol/data/push/appdata"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @addtogroup CAPI_MESSAGING_PUSH_MODULE
 * @{
 */

/**
 * @file push.h
 * @ingroup CAPI_MESSAGING_FRAMEWORK
 * @brief Support to receive push notifications
 */

/**
 * @brief Enumerations of error codes for push API
 */
typedef enum {
	PUSH_ERROR_NONE = 0,   /**< Successful */
	PUSH_ERROR_OUT_OF_MEMORY = -ENOMEM,   /**< Out of memory */
	PUSH_ERROR_INVALID_PARAMETER = -EINVAL,   /**< Invalid parameter */
	PUSH_ERROR_NOT_CONNECTED = -ENOTCONN,  /**< Not connected */
	PUSH_ERROR_NO_DATA = -ENODATA,  /**< No data available */
	PUSH_ERROR_OPERATION_FAILED = -0x00004300, /**< Internal operation failed */
} push_error_e;

/**
 * @brief Enumerations of registration state
 */
typedef enum {
	PUSH_STATE_REGISTERED,   /**< Registred */
	PUSH_STATE_UNREGISTERED, /**< Unregistered */
	PUSH_STATE_ERROR,       /**< Error */
} push_state_e;

/**
 * @brief Enumerations of result
 */
typedef enum {
	PUSH_RESULT_SUCCESS,  /**< Successful */
	PUSH_RESULT_TIMEOUT,  /**< Request timed out */
	PUSH_RESULT_SERVER_ERROR,  /**< Push server error */
	PUSH_RESULT_SYSTEM_ERROR,  /**< System error */
} push_result_e;

/**
 * @brief Handle of a connection to the push service
 */
typedef struct push_connection_s *push_connection_h;

/**
 * @brief Handle of a notification delivered from the push server
 */
typedef struct push_notification_s *push_notification_h;

/**
 * @brief State callback
 * @remarks This callback will be invoked when the regisration state is
 * refreshed. If the registration or degistration has been succeeded,
 * then this state callback must be called. In addition, the state
 * can be changed if the push server deregisters the application.
 * @param[in] state Registration state
 * @param[in] err  Error message
 * @param[in] user_data User data passed to this callback
 * @see push_connect()
 */
typedef void (*push_state_cb)(
		push_state_e state, const char *err, void *user_data);

/**
 * @brief Notifcation callback
 * @param[in] notification A handle of notification containing its payload.
 * The handle is available inside this callback only.
 * @param[in] user_data User data passed to this callback
 * @see push_connect(), push_get_notification_data()
 */
typedef void (*push_notify_cb)(
		push_notification_h noti, void *user_data);

/**
 * @brief Result callback
 * @param[in] result Registration/deregistration result
 * @param[in] msg Result message from the push server or NULL
 * @param[in] user_data User data passed to this callback
 * @see push_register(), push_deregister()
 */
typedef void (*push_result_cb)(push_result_e result, const char *msg, void *user_data);

/**
 * @brief Connects to the push service and sets callback functions
 * @remarks If there is a connection between an application and the push service,
 * the notify callback passes the notification upon its arrival.
 * Otherwise, the push service posts a UI notification to alert users.
 * Connection should be freed with @ref push_disconnect() by you.
 * @param[in] app_id The application ID
 * @param[in] state_cb State callback function
 * @param[in] notify_cb Notify callback function
 * @param[in] user_data User data to pass to <I>state_cb</I> and <I>notify_cb</I>
 * @param[out] connection The connection handle to the push service
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_OPERATION_FAILED Operation failed
 * @pre There is no connection for the <I>app_id</I> to the push service
 * @post The state callback will be called to let you know the current
 * registration state immediately.
 * @see push_disconnect()
 */
int push_connect(const char *app_id, push_state_cb state_callback,
		push_notify_cb notify_callback, void *user_data,
		push_connection_h *connection);

/**
 * @brief Closes the connection and releases all its resources
 * @remarks If you call this function in the push callback functions,
 *          it may cause your application crash.
 * @param[in] connection Handle of a connection to the push service
 * @see push_connect()
 */
void push_disconnect(push_connection_h connection);

/**
 * @brief Registers an application to the push server
 * @param[in] connection The connection handle to the push service
 * @param[in] service A @ref Service handle to launch an application by
 * an posted UI notification
 * @param[in] result_cb  Result callback function
 * @param[in] user_data  User data to pass to <I>result_cb</I>
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NOT_CONNECTED No connection to the push service
 * @retval PUSH_ERROR_OPERATION_FAILED Operation failed
 * @pre The application should be connected to the push service
 * @post For successful result, the state callback should be invoked
 * @see push_deregister()
 */
int push_register(push_connection_h connection,	service_h service,
		push_result_cb result_callback, void *user_data);

/**
 * @brief Deregisters an application from the Push server
 * @param[in] connection The connection handle to the push service
 * @param[in] result_cb Result callback function
 * @param[in] user_data User data to pass to <I>result_cb</I>
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NOT_CONNECTED No connection to the push service
 * @retval PUSH_ERROR_OPERATION_FAILED Operation failed
 * @pre The application should be connected to the push service
 * @post In result, the state callback will be invoked
 * @see push_register()
 */
int push_deregister(push_connection_h connection, push_result_cb callback,
		void *user_data);

/**
 * @brief Gets notification data which its server sent
 * @remark The <I>data</I> must be released with free() by you
 * @param[in] notification The notification handle
 * @param[out] data The notification data\n
 *                  Set NULL if error but <I>PUSH_ERROR_INVALID_PARAMETER</I>
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NO_DATA No data available
 * @see push_notify_cb()
 * @see push_get_unread_notification()
 */
int push_get_notification_data(push_notification_h notification, char **data);


/**
 * @brief Gets the notification message which its server sent
 * @remark The <I>msg</I> must be released with free() by you
 * @param[in] notification The notification handle
 * @param[out] data The notification message\n
 *                  Set NULL if error but <I>PUSH_ERROR_INVALID_PARAMETER</I>
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NO_DATA No data available
 * @see push_notify_cb()
 * @see push_get_unread_notification()
 */
int push_get_notification_message(push_notification_h notification,
		char **msg);

/**
 * @brief Gets the received time of the notification message
 *
 * @param[in] notification The notification handle
 * @param[out] received_time The received time of the notification message. \n
 *                           The @a received_time is based on UTC.
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_NO_DATA No data available
 *
 * @see push_notify_cb()
 * @see push_get_unread_notification()
 */
int push_get_notification_time(push_notification_h notification, long long int *received_time);

/**
 * @brief Gets an unread notification message from the push server
 *
 * @remark This method will be deprecated.
 * @remark @a noti must be released with push_free_notification() by you
 *
 * @details If an application receives an unread message with this method, the message is removed from the system. \n
 *          This method can be called repeatedly until it returns <I>PUSH_ERROR_NO_DATA</I> \n
 *          But, this method does NOT guarantee order and reliability of notification messages. \n
 *          Some notification messages can be dropped when the system message queue is full.
 *
 * @param[in] connection The connection handle to the push service
 * @param[out] noti The notification handle
 * @return 0 on success, otherwise a negative error value.
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NO_DATA No data available
 *
 * @see push_get_notification_message()
 * @see push_get_notification_time()
 * @see push_get_notification_data()
 */
int push_get_unread_notification(push_connection_h connection,
		push_notification_h *noti);


/**
 * @brief Gets the registration ID in <I>PUSH_STATE_REGISTERED</I> state
 * @remark The <I>reg_id</I> must be released with free() by you
 * @param[in] connection The connection handle to the push service
 * @param[out] reg_id The registration ID\n
 *                    Set NULL if error but <I>PUSH_ERROR_INVALID_PARAMETER</I>
 * @return 0 on success, otherwise a negative error value
 * @retval PUSH_ERROR_NONE Successful
 * @retval PUSH_ERROR_INVALID_PARAMETER Invalid parameter
 * @retval PUSH_ERROR_OUT_OF_MEMORY Out of memory
 * @retval PUSH_ERROR_NO_DATA No registration ID available
 */
int push_get_registration_id(push_connection_h connection, char **reg_id);


/**
 * @brief Frees the notification handle
 * @param[in] noti The notification handle
 */
void push_free_notification(push_notification_h noti);
/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#endif /* __PUSH_LIB_H__ */
