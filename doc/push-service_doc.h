/*
 * Copyright (c) 2000 - 2012 Samsung Electronics Co., Ltd All Rights Reserved
 *
 * Licensed under the Apach	e License, Version 2.0 (the "License");
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


#ifndef __PUSH_SERVICE_DOC_H__
#define __PUSH_SERVICE_DOC_H__

/**
 * @ingroup CAPI_MESSAGING_FRAMEWORK
 * @defgroup CAPI_MESSAGING_PUSH_PUBLIC_MODULE Push
 * @brief The @ref CAPI_MESSAGING_PUSH_PUBLIC_MODULE API provides functions to receive push notifications.
 *
 * @addtogroup CAPI_MESSAGING_PUSH_PUBLIC_MODULE
 *
 * @section CAPI_MESSAGING_PUSH_PUBLIC_MODULE_HEADER Required Header
 *   \#include <push-service.h>
 *
 * @section CAPI_MESSAGING_PUSH_PUBLIC_MODULE_OVERVIEW Overview
 *
 * The Push API allows your application to receive push notifications from a push server.
 * The push service is a client daemon that maintains a permanent connection between your device
 * and the push server, in order to process your registration/deregistration requests and
 * deliver push notifications to your application. If the application is connected,
 * the push service passes the notification data over the connection. Otherwise,
 * the push service posts a UI notification with the data.
 * It will be delivered when a user launches the application by selecting the posting.
 *
 * To receive push notifications, you need to follow the steps below:
 *
 * - Connecting to the push service
 * - Registering your application
 * - Getting notification data
 *
 * Push notification helps your application server send data to the application on devices
 * over an IP network even if the application is not running.
 * Push notification may reduce battery consumption over other applications keeping its own connection
 * to its remote application server.
 * @image html capi_messaging_push_overview1.png
 *
 * @subsection CAPI_MESSAGING_PUSH_PUBLIC_LIMITATIONS Service Limitation
 * - Payload of a push message is limited to 4096 bytes.
 * - Administrative permission is needed for your application and server to use the push service.
 * - Push service does not guarantee delivery and order of push messages.
 * - A device should have a valid IMEI number.
 * <BR>
 */

#endif /* __PUSH_SERVICE_DOC_H__ */
