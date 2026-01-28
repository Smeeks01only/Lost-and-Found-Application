import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import api from '../../services/api';
import { Match } from '../../types';

export default function MatchesScreen() {
    const [matches, setMatches] = useState<Match[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchMatches = async () => {
        setLoading(true);
        try {
            const response = await api.get('/matches/');
            setMatches(response.data);
        } catch (error) {
            console.log(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMatches();
    }, []);

    const renderMatch = ({ item }: { item: Match }) => (
        <View style={styles.card}>
            <View style={styles.header}>
                <Text style={styles.score}>Match Score: {item.score.toFixed(2)}</Text>
                <Text style={styles.status}>{item.status}</Text>
            </View>

            <View style={styles.row}>
                <View style={styles.half}>
                    <Text style={styles.label}>Lost Item</Text>
                    <Text style={styles.desc}>{item.lost_item.description}</Text>
                    <Text style={styles.loc}>{item.lost_item.location}</Text>
                </View>
                <View style={styles.divider} />
                <View style={styles.half}>
                    <Text style={styles.label}>Found Item</Text>
                    <Text style={styles.desc}>{item.found_item.description}</Text>
                    <Text style={styles.loc}>{item.found_item.location}</Text>
                </View>
            </View>

            <TouchableOpacity style={styles.actionBtn}>
                <Text style={styles.btnText}>View Details & Verify</Text>
            </TouchableOpacity>
        </View>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Potential Matches (AI)</Text>
            {loading ? <ActivityIndicator size="large" /> : (
                <FlatList
                    data={matches}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={renderMatch}
                    contentContainerStyle={{ paddingBottom: 20 }}
                    ListEmptyComponent={<Text style={styles.empty}>No matches found.</Text>}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 15, backgroundColor: '#f5f5f5' },
    title: { fontSize: 22, fontWeight: 'bold', marginBottom: 15 },
    card: { backgroundColor: '#fff', borderRadius: 12, padding: 15, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.1, elevation: 3 },
    header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10, borderBottomWidth: 1, borderBottomColor: '#eee', paddingBottom: 5 },
    score: { color: '#28a745', fontWeight: 'bold' },
    status: { color: '#666', fontSize: 12, textTransform: 'uppercase' },
    row: { flexDirection: 'row' },
    half: { flex: 1, paddingHorizontal: 5 },
    divider: { width: 1, backgroundColor: '#eee', marginHorizontal: 5 },
    label: { fontSize: 12, color: '#999', marginBottom: 2 },
    desc: { fontSize: 14, fontWeight: '500' },
    loc: { fontSize: 12, color: '#555', marginTop: 2 },
    empty: { textAlign: 'center', marginTop: 50, color: '#999' },
    actionBtn: { marginTop: 15, backgroundColor: '#007AFF', padding: 10, borderRadius: 8, alignItems: 'center' },
    btnText: { color: '#fff', fontWeight: 'bold' }
});
