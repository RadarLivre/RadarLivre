
var radarlivre_updater = function() {
    
    var _ConnectionState = {
        CREATED: 0, 
        RUNNING: 1,
        FINISHED: 2
    }
    
    var _connectionSerial = 0
    var _connectionSet = {}
    
    var _currentObjects = []
    var _onObjectsCreated = function(objects, conn) {}
    var _onObjectsUpdated = function(objects, conn) {}
    var _onObjectsRemoved = function(objects, conn) {}
    
    var _execConnection = function() {
        for(k in _connectionSet) {
            if(_connectionSet[k]._connections.length > 0) {
                var conn = _connectionSet[k]._connections[0];
                if(conn.state === _ConnectionState.CREATED) {
                    conn.state = _ConnectionState.RUNNING;
                    conn.func(conn.id);
                } else if (conn.state === _ConnectionState.FINISHED) {
                    _connectionSet[k]._connections.splice(0, 1);
                }
            }
            
        }
    }
    
    var _getObject = function(dataType, id) {
        return _currentObjects.filter(function(o) {
            return o.dataType === dataType && o.id === id;
        })[0];
    }
    
    var _addObject = function(object) {
        _currentObjects.push(object);
        return object;
    }
    
    var _removeObject = function(object) {
        for(var i = 0; i < _currentObjects.length; i++)
            if(_currentObjects[i].id === object.id) {
                _currentObjects.splice(i, 1);
                break;
            }
    }
    
    var _removeObjects = function(objects) {
        for(o of objects)
            _removeObject(o);
    }
    
    var _getConnection = function(connId, connectionType) {
        if(_connectionSet[connectionType]) {
            for(k in _connectionSet[connectionType]._connections) {
                if(_connectionSet[connectionType]._connections[k].id === connId) {
                    return _connectionSet[connectionType]._connections[k];
                }
            }
        }
        
        return null;
    }
    
    var _createConnection = function(connectionType) {
        var conn = {
            id: _connectionSerial++, 
            requestTimestamp: 0, 
            responseTimestamp: 0, 
            state: _ConnectionState.CREATED
        }
        
        if(!_connectionSet[connectionType])
            _connectionSet[connectionType] = {}
            
        if(!_connectionSet[connectionType]._connections)
            _connectionSet[connectionType]["_connections"] = [];
        
        _connectionSet[connectionType]._connections.push(conn);
        return conn;
    }
    
    var _beginConnection = function(connectionType, connFunc) {
        var conn = _createConnection(connectionType);
        conn["func"] = connFunc;
    }
    
    var _endConnection = function(id, connectionType, data, attrId) {
        if(!attrId)
            attrId = "id";
        var conn = _getConnection(id, connectionType);
        if(conn) {
            conn.state = _ConnectionState.FINISHED;
            conn.responseTimestamp = new Date().getTime();

            var created = []
            var updated = []
            var removed = []
            for(o of data) {
                old = _getObject(connectionType, o[attrId]);
                if(old) {
                    old.data = o;
                    old.timestamp = conn.responseTimestamp;
                    updated.push(o);
                } else {
                    _addObject({
                        dataType: connectionType, 
                        id: o[attrId], 
                        data: o, 
                        timestamp: conn.responseTimestamp
                    });
                    created.push(o);
                }
            }

            removed = _currentObjects.filter(function(o) {
                return o.dataType === connectionType && o.timestamp < conn.responseTimestamp;
            }).map(function(o) {
                return o.data;
            });

            _onObjectsCreated(created, connectionType, conn);
            _onObjectsUpdated(updated, connectionType, conn);
            _onObjectsRemoved(removed, connectionType, conn);

            _removeObjects(removed);
        } else {
            log("Can't end connection: " + connectionType);
        }
    }
    
    var _cancelConnection = function(connectionType) {
        var conn = _getConnection(connectionType);
        conn.state = _ConnectionState.FINISHED;
        conn.responseTimestamp = new Date().getTime();
    }
    
    return {
        doInit : function() {
            setInterval(function() {
                _execConnection();
            }, 100);
        }, 
        
        doGetObject : function(dataType, id) {
            return _getObject(dataType, id);
        }, 
        
        doSetCurrentObjects : function(currentObjects) {
            _currentObjects = currentObjects;
        }, 
        
        doSetOnObjectCreatedListener : function(litener) {
            _onObjectsCreated = litener;
        }, 
        
        doSetOnObjectUpdatedListener : function(litener) {
            _onObjectsUpdated = litener;
        }, 
        
        doSetOnObjectRemovedListener : function(litener) {
            _onObjectsRemoved = litener;
        },
        
        doBeginConnection : function(connectionType, connFunc) {
            return _beginConnection(connectionType, connFunc);
        }, 
        
        doEndConnection : function(connId, connectionType, data, attrId) {
            _endConnection(connId, connectionType, data, attrId);
        }, 
        
        doCancelConnection : function(connId, connectionType) {
            _cancelConnection(connId, connectionType);
        }
        
    }
    
} ();