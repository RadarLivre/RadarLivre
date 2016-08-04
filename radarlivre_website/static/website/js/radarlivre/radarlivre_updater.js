
var radarlivre_updater = function() {
    
    var _ConnectionState = {
        RUNNING: 0, 
        STOPED: 1
    }
    
    var _connectionSet = {}
    
    var _currentObjects = []
    var _onObjectsCreated = function(objects, conn) {}
    var _onObjectsUpdated = function(objects, conn) {}
    var _onObjectsRemoved = function(objects, conn) {}
    
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
    
    var _getConnection = function(connectionType) {
        if(!_connectionSet[connectionType]) {
            _connectionSet[connectionType] = {
                requestTimestamp: 0, 
                state: _ConnectionState.STOPED, 
                responseTimestamp: 0
            }
        }
        return _connectionSet[connectionType];
    }
    
    var _beginConnection = function(connectionType) {
        var conn = _getConnection(connectionType);
        if(conn.state === _ConnectionState.STOPED) {
            conn.requestTimestamp = new Date().getTime();
            conn.state = _ConnectionState.RUNNING;
            return true;
        } 
        return false;
    }
    
    var _endConnection = function(connectionType, data, attrId) {
        if(!attrId)
            attrId = "id";
        var conn = _getConnection(connectionType);
        conn.state = _ConnectionState.STOPED;
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
    }
    
    var _cancelConnection = function(connectionType) {
        var conn = _getConnection(connectionType);
        conn.state = _ConnectionState.STOPED;
        conn.responseTimestamp = new Date().getTime();
    }
    
    return {
        doInit : function() {
            
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
        
        doBeginConnection : function(connectionType) {
            return _beginConnection(connectionType);
        }, 
        
        doEndConnection : function(connectionType, data, attrId) {
            _endConnection(connectionType, data, attrId);
        }, 
        
        doCancelConnection : function(connectionType) {
            _cancelConnection(connectionType);
        }
        
    }
    
} ();