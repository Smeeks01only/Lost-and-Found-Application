import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useAuth } from '../../context/AuthContext';

export default function ProfileScreen() {
    const { user, signOut } = useAuth();

    return (
        <View style={styles.container}>
            <View style={styles.avatar}>
                <Text style={styles.avatarText}>{user?.username?.[0]?.toUpperCase()}</Text>
            </View>
            <Text style={styles.username}>@{user?.username}</Text>
            <Text style={styles.role}>Role: {user?.role}</Text>

            <TouchableOpacity style={styles.logoutBtn} onPress={signOut}>
                <Text style={styles.logoutText}>Log Out</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#fff' },
    avatar: { width: 100, height: 100, borderRadius: 50, backgroundColor: '#eee', alignItems: 'center', justifyContent: 'center', marginBottom: 20 },
    avatarText: { fontSize: 40, fontWeight: 'bold', color: '#555' },
    username: { fontSize: 24, fontWeight: 'bold', marginBottom: 5 },
    role: { fontSize: 16, color: '#666', marginBottom: 40 },
    logoutBtn: { backgroundColor: '#ff4444', paddingVertical: 12, paddingHorizontal: 40, borderRadius: 25 },
    logoutText: { color: '#fff', fontSize: 16, fontWeight: 'bold' }
});
