
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('username').addEventListener('input', checkRegisterConditions);
    document.getElementById('password').addEventListener('input', checkRegisterConditions);
    document.getElementById('regist').addEventListener('click', create_user);
    document.getElementById('searchButton').addEventListener('click', searchEvents);
    document.getElementById('updateButton').addEventListener('click', updateEvents);
    document.getElementById('deleteButton').addEventListener('click', deleteEvents);
    bindEditableEvents(); 
    bindSelectAllEvent();
});


// 登入彈出視窗顯示
function showLoginModal() {
    $('#loginModal').modal('show');  
}

// 綁定編輯表格
function bindEditableEvents() {
    document.querySelectorAll('#eventsTable td').forEach(td => {
        td.addEventListener('dblclick', function () {
            if (!this.classList.contains('uid-column')) { 
                if (!this.hasAttribute('contenteditable')) {
                    this.setAttribute('contenteditable', 'true');
                    this.classList.add("editable");
                    this.focus();
                }
            }
        });

        td.addEventListener('blur', function () {
            this.removeAttribute('contenteditable');
        });
    });
}

// 綁定選取表格
function bindSelectAllEvent() {
    document.getElementById('selectAll').addEventListener('change', function() {
        document.querySelectorAll('.selectRow').forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
}

// showinfo表格
function loadEventDetails(eventUID) {
    let eventDataElement = document.getElementById(`event-data-${eventUID}`);
    let eventDataText = eventDataElement.innerText;
    eventDataText = eventDataText.replace(/'/g, '"').replace(/None/g, "null").replace(/,\.\.\.]$/, "]");
    let eventsArray = JSON.parse(eventDataText);

    try {
        $("#exampleModal .modal-title").text('Event Details');
        let tableBody = $("#exampleModal #modalTable tbody");
        tableBody.empty();

        // 創建欄位
        eventsArray.forEach(event => {
            let row = `<tr>
                <td>${event.time|| "None"}</td>
                <td>${event.locationName|| "None"}</td>
                <td>${event.onSales|| "None"}</td>
                <td>${event.price|| "None"}</td>
                <td>${event.endTime|| "None"}</td>
            </tr>`;
            tableBody.append(row); 
        });

        var myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
        myModal.show();

    } catch (e) {
        console.error("Error: ", e);
    }
}

// login 邏輯
function handleLogin(e) {
    e.preventDefault(); 

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    console.log(username, password)
    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // 确保添加 CSRF 令牌
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();  // 解析响应为 JSON
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            window.location.reload();  // 如果登录成功，重新加载页面
        } else {
            document.getElementById('loginMessage').innerText = data.message;  // 如果登录失败，显示错误信息
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

// 註冊用戶
function create_user(e) {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/create_user/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // 确保包含 CSRF 令牌
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        var messageElement = document.getElementById('loginMessage');
        if (data.success) {
            messageElement.innerText = data.message; 
            window.location.reload();
        } else {
            messageElement.innerText = data.message;  // 显示错误信息
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
};

// 獲取 CSRF 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');  // 獲取CSRF

// 密碼複雜度檢查
function checkRegisterConditions() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var registerButton = document.getElementById('regist');
    var message = '';

    // 檢查密碼複雜度
    if (!/[A-Za-z]/.test(password) || !/\d/.test(password) || password.length < 8) {
        message = '密碼過於簡單。 密碼必須包含字母、數字，且長度至少為 8 個字符。';
    }

    // 檢查Username 與password 長度
    if (username.length < 5 || password.length < 8) {
        registerButton.disabled = true;
        message += '\n使用者名稱長度至少為 5 個字符，密碼長度至少為 8 個字符。';
    } else {
        registerButton.disabled = false;
    }
    document.getElementById('passwordHelp').innerText = message;
}

// 搜尋函式
function searchEvents() {
    var searchQuery = document.getElementById('searchInput').value;
    fetch('/operation/?query=' + encodeURIComponent(searchQuery))
    .then(response => {
        // console.log(response)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  
    })
    .then(data => {  // 修改这里，将参数改为 data
        console.log(data);  // 查看完整的数据结构
        var html = '';
        // 使用 data.events 访问事件数组
        data.events.forEach(event => {  // 修改这里，使用 data.events 而不是 events
            html += `<tr>
                        <td>${event.UID}</td>
                        <td>${event.title}</td>
                        <td>${event.category}</td>
                        <td>${event.descriptionFilterHtml}</td>
                        <td><a href="${event.webSales}" target="_blank">Ticket Link</a></td>
                        <td>${event.startDate}</td>
                        <td>${event.endDate}</td>
                        <td>
                            <button type="button" class="btn btn-info" onclick="loadEventDetails('${event.UID}')">
                                Show Details
                            </button>
                            <div id="event-data-${event.UID}" style="display: none;">
                                ${JSON.stringify(event.shows)}  <!-- 使用 JSON.stringify 来处理 shows 数组 -->
                            </div>
                        </td>
                    </tr>`;
        });
        document.querySelector('#eventsTable tbody').innerHTML = html;
        bindEditableEvents();
        bindSelectAllEvent();
    })
    .catch(error => console.error('Error:', error));
}

// 更新函式
function updateEvents() {
    const editedCells = document.querySelectorAll('#eventsTable .editable');
    const updatedRows = new Set();  // 用来存储被编辑过的行

    editedCells.forEach(cell => {
        updatedRows.add(cell.closest('tr'));  // 添加这个单元格所在的行到集合中
    });

    const updatedEvents = Array.from(updatedRows).map(row => {
        const cells = row.querySelectorAll('td');
        return {
            UID: cells[0].innerText,  
            title: cells[1].innerText, 
            category: cells[2].innerText,  
            description: cells[3].innerText,  
            startDate: cells[5].innerText,  
            endDate: cells[6].innerText 
        };
    });
    console.log(editedCells);
    console.log(updatedEvents);
    fetch('/operation/', {  
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({events: updatedEvents})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  
    })
    .then(data => {
        console.log('Update successful:', data);
        alert('資料修改成功');
        editedCells.forEach(cell => cell.classList.remove('editable'));
        document.querySelectorAll('#eventsTable .editable').forEach(cell => {
            cell.classList.remove("editable");
            cell.removeAttribute('contenteditable');
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 刪除函式
function deleteEvents() {
    const selectedUIDs = Array.from(document.querySelectorAll('.selectRow:checked')).map(cb => cb.dataset.uid);
    console.log(selectedUIDs);

    if (selectedUIDs.length === 0) {
        alert('請選擇至少一條記錄進行刪除！');
        return;
    }

    const confirmation = confirm('確定要刪除選中的記錄嗎？');
    if (!confirmation) {
        return;
    }

    fetch('/operation/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // 確保 CSRF 令牌被包含
        },
        body: JSON.stringify({UIDs: selectedUIDs})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Delete successful:', data);
        alert('刪除成功');
        // 移除已刪除的行
        selectedUIDs.forEach(uid => {
            document.querySelector(`tr[data-uid="${uid}"]`).remove();
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
